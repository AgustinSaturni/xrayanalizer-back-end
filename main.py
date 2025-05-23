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

# Modelo para los ángulos
class Angle(BaseModel):
    name: str
    value: str

# Modelo para un reporte
class Report(BaseModel):
    id: int
    name: str
    projectName: str
    patientId: str
    date: str
    imageCount: int
    projectId: str
    angles: List[Angle]
    notes: str

class ReportCreate(BaseModel):
    projectId: str
    projectName: str
    patientId: str
    name: str
    imageCount: int
    angles: List[Angle]
    notes: str

class ReportUpdate(BaseModel):
    projectId: Optional[str] = None
    projectName: Optional[str] = None
    patientId: Optional[str] = None
    name: Optional[str] = None
    imageCount: Optional[int] = None
    angles: Optional[List[Angle]] = None
    notes: Optional[str] = None

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

# Simulación de base de datos de reportes
reports = [
    Report(
        id=1,
        name= "nombre prueba 1",
        projectName="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        imageCount=3,
        projectId="1",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="23°"),
            Angle(name="Ángulo Intermetatarsiano", value="12°"),
            Angle(name="Ángulo PASA", value="8°"),
            Angle(name="Ángulo DASA", value="6°"),
        ],
        notes="El paciente presenta un hallux valgus moderado en el pie derecho.",
    ),
    Report(
        id=2,
        name="nombre prueba 2",
        projectName="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        imageCount=1,
        projectId="1",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="18°"),
            Angle(name="Ángulo Intermetatarsiano", value="10°"),
            Angle(name="Ángulo PASA", value="7°"),
            Angle(name="Ángulo DASA", value="5°"),
        ],
        notes="Seguimiento del paciente A, se observa mejoría.",
    ),
    Report(
        id=3,
        name= "nombre prueba 3",
        projectName="Paciente B - Seguimiento",
        patientId="PAC-002",
        date="10/04/2025",
        imageCount=2,
        projectId="2",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="15°"),
            Angle(name="Ángulo Intermetatarsiano", value="9°"),
            Angle(name="Ángulo PASA", value="6°"),
            Angle(name="Ángulo DASA", value="4°"),
        ],
        notes="Evaluación de seguimiento del paciente B.",
    ),
    Report(
        id=4,
        name= "nombre prueba 4",
        projectName="Paciente C - Post-operatorio",
        patientId="PAC-003",
        date="05/04/2025",
        imageCount=4,
        projectId="3",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="8°"),
            Angle(name="Ángulo Intermetatarsiano", value="7°"),
            Angle(name="Ángulo PASA", value="5°"),
            Angle(name="Ángulo DASA", value="3°"),
        ],
        notes="Evaluación post-operatoria, resultados satisfactorios.",
    ),
    Report(
        id=5,
        name= "nombre prueba 5",
        projectName="Paciente D - Evaluación Pre-quirúrgica",
        patientId="PAC-004",
        date="01/04/2025",
        imageCount=2,
        projectId="4",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="28°"),
            Angle(name="Ángulo Intermetatarsiano", value="15°"),
            Angle(name="Ángulo PASA", value="10°"),
            Angle(name="Ángulo DASA", value="8°"),
        ],
        notes="Evaluación pre-quirúrgica, se recomienda intervención.",
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


# 🗑️ Eliminar un proyecto por ID
@app.delete("/projects/{project_id}", response_model=bool)
def delete_project(project_id: str):
    print("Eliminando proyecto con ID:", project_id)
    for index, project in enumerate(projects):
        if project.id == project_id:
            deleted_project = projects.pop(index)
            print("Proyecto eliminado:", deleted_project)
            return True
    print("Proyecto no encontrado para eliminar con ID:", project_id)
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


# Endpoint para obtener todos los reportes
@app.get("/reports", response_model=List[Report])
def get_reports():
    return reports

# Endpoint para obtener un reporte por id
@app.get("/reports/{report_id}", response_model=Report)
def get_report_by_id(report_id: int):
    for report in reports:
        if report.id == report_id:
            return report
    raise HTTPException(status_code=404, detail="Reporte no encontrado")

# Endpoint para obtener todos los reportes asociados a un proyecto id
@app.get("/reports/by_project/{project_id}", response_model=List[Report])
def get_reports_by_project_id(project_id: str):
    filtered_reports = [report for report in reports if report.projectId == project_id]
    return filtered_reports

# Endpoint para eliminar un reporte por id
@app.delete("/reports/{report_id}", response_model=Report)
def delete_report(report_id: int):

    global reports  # para poder modificar la lista

    # Buscar el índice del reporte
    report_index = next((i for i, r in enumerate(reports) if r.id == report_id), None)

    if report_index is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Guardar el reporte eliminado
    deleted_report = reports[report_index]

    # Eliminar el reporte
    reports = [r for r in reports if r.id != report_id]

    # Simular la actualización del contador de reportes del proyecto relacionado
    for project in projects:
        if project.id == deleted_report.projectId and project.reportCount > 0:
            project.reportCount -= 1
            break

    return deleted_report

# Endpoint para crear un reporte
@app.post("/reports", response_model=int)
def create_report(report_data: ReportCreate):
    # Generar nuevo ID único
    new_id = max([r.id for r in reports], default=0) + 1

    # Crear nuevo objeto Report
    new_report = Report(
        id=new_id,
        date=datetime.now().strftime("%d/%m/%Y"),  # formato "es-ES"
        **report_data.dict()
    )

    reports.append(new_report)

    # Actualizar el contador de reportes en el proyecto relacionado
    for project in projects:
        if project.id == report_data.projectId:
            project.reportCount = getattr(project, "reportCount", 0) + 1
            break

    return new_id

# Endpoint para editar un reporte
@app.put("/reports/{id}")
def update_report(id: int, report_data: ReportUpdate):
    for index, report in enumerate(reports):
        if report.id == id:
            updated_report_data = report.dict()
            update_fields = report_data.dict(exclude_unset=True)

            # Actualizamos solo los campos que vinieron en el body
            updated_report_data.update(update_fields)

            # Creamos una nueva instancia para mantener validación
            reports[index] = Report(**updated_report_data)

            return reports[index]

    raise HTTPException(status_code=404, detail="Reporte no encontrado")