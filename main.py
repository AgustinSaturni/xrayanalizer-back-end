from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import time
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés restringirlo a ["http://localhost:3000"] si querés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo base para recibir los datos del nuevo proyecto
class ProjectCreate(BaseModel):
    name: str
    patientId: str
    description: str

# Modelo completo para responder
class Project(ProjectCreate):
    id: str
    date: str
    imageCount: int
    reportCount: int

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    patientId: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    imageCount: Optional[int] = None
    reportCount: Optional[int] = None

# Simulación de una base de datos en memoria
projects = [
    Project(
        id="1",
        name="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        description="Evaluación inicial del paciente A",
        imageCount=0,
        reportCount=0
    ),
    Project(
        id="2",
        name="Paciente B - Seguimiento",
        patientId="PAC-002",
        date="10/04/2025",
        description="Seguimiento del paciente B",
        imageCount=0,
        reportCount=0
    ),
    Project(
        id="3",
        name="Paciente C - Post-operatorio",
        patientId="PAC-003",
        date="05/04/2025",
        description="Evaluación post-operatoria del paciente C",
        imageCount=0,
        reportCount=0
    ),
]
# Endpoint para obtener todos los proyectos
@app.get("/projects", response_model=List[Project])
def get_projects():
    return projects


# 🆕 Endpoint para crear un nuevo proyecto
@app.post("/projects", response_model=str)
def create_project(project_data: ProjectCreate):
    new_id = str(int(time.time() * 1000))  # ID único basado en timestamp
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
@app.get("/projects/{project_id}", response_model=Project)
def get_project_by_id(project_id: str):
    for project in projects:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    
# 🆕 Actualizar un proyecto por ID
@app.put("/projects/{project_id}", response_model=Project)
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
