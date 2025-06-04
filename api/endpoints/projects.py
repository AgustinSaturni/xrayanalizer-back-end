from fastapi import APIRouter, HTTPException,Depends
from models.project import Project, ProjectCreate, ProjectUpdate
from datetime import date, datetime
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
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    # Crear instancia del modelo ORM
    new_project = ProjectORM(
        name=project_data.name,
        patientId=project_data.patientId,
        description=project_data.description,
        date=date.today(),  # fecha de hoy como objeto date
        imageCount=0,
        reportCount=0
    )
    
    # Agregar y guardar en base de datos
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Devolver el ID generado por la base de datos
    return str(new_project.id)

# 🆕 Obtener un proyecto por ID
@router.get("/{projectId}", response_model=Project)
def get_project_by_id(projectId: int, db: Session = Depends(get_db)):
    project = db.query(ProjectORM).filter(ProjectORM.id == projectId).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return project

# 🆕 Actualizar un proyecto por ID
@router.put("/{projectId}", response_model=Project)
def update_project(projectId: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    # Buscar proyecto existente
    project = db.query(ProjectORM).filter(ProjectORM.id == projectId).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Aplicar actualizaciones
    update_data = project_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project

# 🗑️ Eliminar un proyecto por ID
@router.delete("/{projectId}", response_model=bool)
def delete_project(projectId: int, db: Session = Depends(get_db)):
    print("Eliminando proyecto con ID:", projectId)

    project = db.query(ProjectORM).filter(ProjectORM.id == projectId).first()

    if not project:
        print("Proyecto no encontrado para eliminar con ID:", projectId)
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    db.delete(project)
    db.commit()
    print("Proyecto eliminado:", project)
    return True