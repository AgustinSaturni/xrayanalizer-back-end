from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from models.image import Image
from db.fake_db import images_db
from datetime import datetime
import base64
import uuid
from db.fake_db import projects

router = APIRouter()

@router.post("/upload", response_model=str)
async def upload_image(file: UploadFile = File(...), projectId: str = Form(...)):
    try:
        content = await file.read()
        base64_content = base64.b64encode(content).decode("utf-8")
        data_url = f"data:{file.content_type};base64,{base64_content}"

        image_id = f"{uuid.uuid4().hex}"

        image = Image(
            id=image_id,
            projectId=projectId,
            name=file.filename,
            url=data_url,
            type=file.content_type,
            size=len(content),
            uploadedAt=datetime.utcnow(),
        )
        images_db.append(image)
        return image.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project/{project_id}", response_model=List[Image])
async def get_project_images(project_id: str):
    return [img for img in images_db if img.projectId == project_id]

@router.delete("/{image_id}")
async def delete_image(image_id: str):
    # Buscar imagen
    image_to_delete = None
    for img in images_db:
        if img.id == image_id:
            image_to_delete = img
            break

    if not image_to_delete:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Eliminar imagen
    images_db.remove(image_to_delete)

    # Actualizar contador de imágenes en proyecto
    for project in projects:
        if project.id == image_to_delete.projectId:
            if project.imageCount > 0:
                project.imageCount -= 1
            break

    return {"detail": "Imagen eliminada correctamente"}
