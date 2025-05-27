from fastapi import APIRouter, HTTPException,Depends
from models.project import Project, ProjectCreate, ProjectUpdate
from db.fake_db import projects
from datetime import datetime
import time
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.project import Project, ProjectORM

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[Project])
def get_projects(db: Session = Depends(get_db)):
    return db.query(ProjectORM).all()

@router.post("", response_model=str)
def create_project(project_data: ProjectCreate):
    new_id = str(int(time.time() * 1000))
    new_project = Project(
        id=new_id,
        name=project_data.name,
        patientId=project_data.patientId,
        description=project_data.description,
        date=datetime.now().strftime("%d/%m/%Y"),
        imageCount=0,
        reportCount=0
    )
    projects.append(new_project)
    return new_id

# 🆕 Obtener un proyecto por ID
@router.get("/{project_id}", response_model=Project)
def get_project_by_id(project_id: str):
    for project in projects:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")

# 🆕 Actualizar un proyecto por ID
@router.put("/{project_id}", response_model=Project)
def update_project(project_id: str, project_data: ProjectUpdate):
    print("Actualizando proyecto con ID:", project_id)
    for index, project in enumerate(projects):
        if project.id == project_id:
            updated_project = project.copy(update=project_data.dict(exclude_unset=True))
            projects[index] = updated_project
            print("Proyecto actualizado:", updated_project)
            return updated_project
    print("Proyecto no encontrado:", project_id)
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


# 🗑️ Eliminar un proyecto por ID
@router.delete("/{project_id}", response_model=bool)
def delete_project(project_id: str):
    print("Eliminando proyecto con ID:", project_id)
    for index, project in enumerate(projects):
        if project.id == project_id:
            deleted_project = projects.pop(index)
            print("Proyecto eliminado:", deleted_project)
            return True
    print("Proyecto no encontrado para eliminar con ID:", project_id)
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")
