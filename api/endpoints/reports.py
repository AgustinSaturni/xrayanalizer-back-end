from fastapi import APIRouter,Depends, HTTPException
from db.database import SessionLocal
from models.report import Angle, MeasurementORM, Report, ReportCreate,ReportUpdate
from db.fake_db import projects
from datetime import datetime
from typing import List
from models.report import Report, ReportORM
from sqlalchemy.orm import Session

router = APIRouter(prefix="", tags=["Reports"])

# Dependency para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener todos los reportes
@router.get("/", response_model=List[Report])
def get_all_reports(db: Session = Depends(get_db)):
    reports_orm = db.query(ReportORM).all()
    
    if not reports_orm:
        raise HTTPException(status_code=404, detail="No reports found")

    reports = []
    for report in reports_orm:
        angles = [
            Angle(name=m.angle.name, value=m.value)
            for m in report.measurements
        ]

        reports.append(
            Report(
                id=report.id,
                name=report.name,
                projectName=report.project.name if report.project else None,
                patientId=report.patientid,
                date=report.date,
                imageCount=report.image_count,
                projectId=report.projectid,
                notes=report.notes,
                angles=angles,
            )
        )

    return reports


# Endpoint para obtener un reporte por id
@router.get("/{report_id}", response_model=Report)
def get_report_by_id(report_id: int, db: Session = Depends(get_db)):
    report = db.query(ReportORM).filter(ReportORM.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    angles = [
        Angle(name=m.angle.name, value=m.value)
        for m in report.measurements
    ]

    return Report(
        id=report.id,
        name=report.name,
        projectName=report.project.name if report.project else None,
        patientId=report.patientid,
        date=report.date,
        imageCount=report.image_count,
        projectId=report.projectid,
        notes=report.notes,
        angles=angles,
    )


# Endpoint para obtener todos los reportes asociados a un proyecto id
@router.get("/by_project/{project_id}", response_model=List[Report])
def get_reports_by_project_id(project_id: int, db: Session = Depends(get_db)):
    reports_orm = db.query(ReportORM).filter(ReportORM.projectid == project_id).all()

    if not reports_orm:
        raise HTTPException(status_code=404, detail="No hay reportes para este proyecto")

    reports = []
    for report in reports_orm:
        angles = [
            Angle(name=m.angle.name, value=m.value)
            for m in report.measurements
        ]

        reports.append(
            Report(
                id=report.id,
                name=report.name,
                projectName=report.project.name if report.project else None,
                patientId=report.patientid,
                date=report.date,
                imageCount=report.image_count,
                projectId=report.projectid,
                notes=report.notes,
                angles=angles,
            )
        )

    return reports


# Endpoint para eliminar un reporte por id
@router.delete("/{report_id}", response_model=Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    # Buscar el reporte en la base
    report = db.query(ReportORM).filter(ReportORM.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Crear el objeto Report a retornar (antes de eliminarlo)
    angles = [
        Angle(name=m.angle.name, value=m.value)
        for m in report.measurements
    ]
    deleted_report = Report(
        id=report.id,
        name=report.name,
        projectName=report.project.name if report.project else None,
        patientId=report.patientid,
        date=report.date,
        imageCount=report.image_count,
        projectId=report.projectid,
        notes=report.notes,
        angles=angles,
    )

    # Eliminar mediciones asociadas
    db.query(MeasurementORM).filter(MeasurementORM.reportid == report.id).delete()

    # Eliminar el reporte
    db.delete(report)

    # Decrementar el contador si corresponde
    if report.project and report.project.report_count > 0:
        report.project.report_count -= 1

    # Confirmar todos los cambios
    db.commit()

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
