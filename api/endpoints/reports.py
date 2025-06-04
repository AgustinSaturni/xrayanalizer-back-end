from fastapi import APIRouter,Depends, HTTPException
from db.database import SessionLocal
from models.project import ProjectORM
from models.report import Angle, AngleORM, MeasurementORM, Report, ReportCreate,ReportUpdate
from datetime import date, datetime
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
@router.get("", response_model=List[Report])
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
                patientId=report.patientId,
                date=report.date,
                imageCount=report.imageCount,
                projectId=report.projectId,
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
        patientId=report.patientId,
        date=report.date,
        imageCount=report.imageCount,
        projectId=report.projectId,
        notes=report.notes,
        angles=angles,
    )


# Endpoint para obtener todos los reportes asociados a un proyecto id
@router.get("/by_project/{projectId}", response_model=List[Report])
def get_reports_by_project_id(projectId: int, db: Session = Depends(get_db)):
    reports_orm = db.query(ReportORM).filter(ReportORM.projectId == projectId).all()

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
                patientId=report.patientId,
                date=report.date,
                imageCount=report.imageCount,
                projectId=report.projectId,
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
        patientId=report.patientId,
        date=report.date,
        imageCount=report.imageCount,
        projectId=report.projectId,
        notes=report.notes,
        angles=angles,
    )

    # Eliminar mediciones asociadas
    db.query(MeasurementORM).filter(MeasurementORM.reportId == report.id).delete()

    # Eliminar el reporte
    db.delete(report)

    # Decrementar el contador si corresponde
    if report.project and report.project.reportCount > 0:
        report.project.reportCount -= 1

    # Confirmar todos los cambios
    db.commit()

    return deleted_report


@router.post("", response_model=int)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    # Verificar si el proyecto existe
    project = db.query(ProjectORM).filter(ProjectORM.id == report_data.projectId).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Crear el nuevo reporte
    new_report = ReportORM(
        name=report_data.name,
        patientId=report_data.patientId,
        date=report_data.date or date.today(),
        imageCount=report_data.imageCount,
        notes=report_data.notes,
        projectId=report_data.projectId
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)  # Obtener el ID generado

    # Crear mediciones (Measurements)
    for angle in report_data.angles:
        # Buscar el ángulo en la tabla angulo
        angle_orm = db.query(AngleORM).filter(AngleORM.name == angle.name).first()
        if not angle_orm:
            raise HTTPException(status_code=400, detail=f"Ángulo '{angle.name}' no encontrado")

        measurement = MeasurementORM(
            value=angle.value,
            date=report_data.date,
            angleId=angle_orm.id,
            reportId=new_report.id
        )
        db.add(measurement)

    # Actualizar contador de reportes del proyecto
    project.reportCount = (project.reportCount or 0) + 1
    db.commit()

    return new_report.id


# Endpoint para editar un reporte
@router.put("/{id}", response_model=Report)
def update_report(id: int, report_data: ReportUpdate, db: Session = Depends(get_db)):
    # Buscar el reporte existente
    report = db.query(ReportORM).filter(ReportORM.id == id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # Guardamos el ID del proyecto anterior (por si se cambia el proyecto)
    old_project_id = report.projectId

    # Aplicar actualizaciones al objeto ReportORM
    update_fields = report_data.dict(exclude_unset=True, by_alias=False)
    print("Campos a actualizar:", update_fields)
    for field, value in update_fields.items():
        if field == "angles":
            continue  # Los angles se procesan aparte
        setattr(report, field, value)

    # Actualizar mediciones si vienen nuevas
    if report_data.angles is not None:
        # Eliminar mediciones actuales
        db.query(MeasurementORM).filter(MeasurementORM.reportId == report.id).delete()

        # Agregar nuevas mediciones
        for angle in report_data.angles:
            # Buscar el ángulo en la base
            angle_obj = db.query(AngleORM).filter(AngleORM.name == angle.name).first()
            if not angle_obj:
                raise HTTPException(status_code=404, detail=f"Ángulo '{angle.name}' no encontrado")

            new_measurement = MeasurementORM(
                value=angle.value,
                reportId=report.id,
                angleId=angle_obj.id
            )
            db.add(new_measurement)

    # Si cambió el proyecto, actualizar los contadores
    new_project_id = report_data.projectId if report_data.projectId is not None else old_project_id

    if old_project_id != new_project_id:
        # Decrementar el contador del proyecto anterior
        old_project = db.query(ProjectORM).filter(ProjectORM.id == old_project_id).first()
        if old_project and old_project.reportCount > 0:
            old_project.reportCount -= 1

        # Incrementar el contador del nuevo proyecto
        new_project = db.query(ProjectORM).filter(ProjectORM.id == new_project_id).first()
        if new_project:
            new_project.reportCount += 1

    db.commit()
    db.refresh(report)

    # Armar el response con las mediciones actualizadas
    angles = [
        Angle(name=m.angle.name, value=m.value)
        for m in report.measurements
    ]

    return Report(
        id=report.id,
        name=report.name,
        projectName=report.project.name if report.project else None,
        patientId=report.patientId,
        date=report.date,
        imageCount=report.imageCount,
        projectId=report.projectId,
        notes=report.notes,
        angles=angles,
    )
