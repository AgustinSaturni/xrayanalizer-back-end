from tkinter import Image
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import base64
from api.endpoints.projects import get_db
from models.image import ImageORM
from models.project import ProjectORM


router = APIRouter()

@router.post("/upload", response_model=str)
async def upload_image(file: UploadFile = File(...), projectId: str = Form(...), db: Session = Depends(get_db)):
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
            uploadedat=datetime.utcnow().date(),  # La columna es tipo DATE
        )

        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return new_image.url

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



