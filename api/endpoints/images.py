from models.image import Image 
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import base64
from api.endpoints.projects import get_db
from models.image import ImageORM
from models.project import ProjectORM

router = APIRouter()

#Alta de imagen
@router.post("/upload", response_model=str)
async def upload_image(file: UploadFile = File(...), projectId: int = Form(...), db: Session = Depends(get_db)):
    try:
        # Verificar si el proyecto existe
        project = db.query(ProjectORM).filter(ProjectORM.id == int(projectId)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        # Leer el contenido del archivo
        content = await file.read()
        base64_content = base64.b64encode(content).decode("utf-8")
        data_url = f"data:{file.content_type};base64,{base64_content}"

        # Crear y guardar en la base de datos
        new_image = ImageORM(
            projectId=int(projectId),
            name=file.filename,
            url=data_url,
            size=len(content),
            uploadedDate=datetime.utcnow().date(),  # La columna es tipo DATE
        )
        db.add(new_image)

        # 🟢 Incrementar el contador de imágenes del proyecto
        project.imageCount = (project.imageCount or 0) + 1

        db.commit()
        db.refresh(new_image)

        return new_image.url

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#GetAll de imagenes de un proyecto
@router.get("/project/{project_id}", response_model=List[Image])
def get_project_images(project_id: int, db: Session = Depends(get_db)):
    # Verificar si el proyecto existe
    project = db.query(ProjectORM).filter(ProjectORM.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Consultar imágenes del proyecto
    images = db.query(ImageORM).filter(ImageORM.projectId == project_id).all()

    return images

#Delete de todas las imagenes de un proyecto
@router.delete("/project/{project_id}/images", status_code=204)
def delete_project_images(project_id: int, db: Session = Depends(get_db)):
    # Verificar si el proyecto existe
    project = db.query(ProjectORM).filter(ProjectORM.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Obtener imágenes asociadas al proyecto
    images = db.query(ImageORM).filter(ImageORM.projectId == project_id).all()

    if not images:
        raise HTTPException(status_code=404, detail="No hay imágenes asociadas a este proyecto")

    # Eliminar las imágenes
    for image in images:
        db.delete(image)

    # 🟢 Restar el contador de imágenes
    project.imageCount = max((project.imageCount or 0) - len(images), 0)

    db.commit()
    return  # status 204: No Content

#Delete de una imagen por id
@router.delete("/{image_id}", response_model=Image, status_code=200)
def delete_image_by_id(image_id: int, db: Session = Depends(get_db)):
    # Buscar la imagen por ID
    image = db.query(ImageORM).filter(ImageORM.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Obtener el proyecto relacionado
    project = db.query(ProjectORM).filter(ProjectORM.id == image.projectId).first()
    if project and project.imageCount > 0:
        project.imageCount -= 1

    # Guardar una copia del contenido antes de eliminar
    image_data = Image(
        id=image.id,
        name=image.name,
        url=image.url,
        projectId=image.projectId,
        uploadedDate=image.uploadedDate,
        size=image.size
    )

    # Eliminar la imagen
    db.delete(image)
    db.commit()

    return image_data

