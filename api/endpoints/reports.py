from fastapi import APIRouter, HTTPException
from models.report import Report, ReportCreate,ReportUpdate
from db.fake_db import reports, projects
from datetime import datetime
from typing import List

router = APIRouter()

# Endpoint para obtener todos los reportes
@router.get("", response_model=List[Report])
def get_reports():
    return reports

# Endpoint para obtener un reporte por id
@router.get("/{report_id}", response_model=Report)
def get_report_by_id(report_id: int):
    for report in reports:
        if report.id == report_id:
            return report
    raise HTTPException(status_code=404, detail="Reporte no encontrado")

# Endpoint para obtener todos los reportes asociados a un proyecto id
@router.get("/by_project/{project_id}", response_model=List[Report])
def get_reports_by_project_id(project_id: str):
    filtered_reports = [report for report in reports if report.projectId == project_id]
    return filtered_reports

# Endpoint para eliminar un reporte por id
@router.delete("/{report_id}", response_model=Report)
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
@router.post("", response_model=int)
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
@router.put("/{id}")
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
