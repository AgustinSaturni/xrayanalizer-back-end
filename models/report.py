from pydantic import BaseModel,Field
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import date as dt_date


class ReportORM(Base):
    __tablename__ = "reporte"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    patientId = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    imageCount = Column(Integer, default=0)
    projectId = Column(Integer, ForeignKey("proyecto.id"), nullable=False)
    notes = Column(String)

    # Relaciones
    project = relationship("ProjectORM", back_populates="reports")
    measurements = relationship("MeasurementORM", back_populates="report",cascade="all, delete-orphan")



class MeasurementORM(Base):
    __tablename__ = "medicion"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)
    date = Column(Date)
    angleId = Column(Integer, ForeignKey("angulo.id"), nullable=False)
    reportId = Column(Integer, ForeignKey("reporte.id"), nullable=False)

    # Relaciones
    report = relationship("ReportORM", back_populates="measurements")
    angle = relationship("AngleORM")

class AngleORM(Base):
    __tablename__ = "angulo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Angle(BaseModel):
    name: str
    value: str


class Report(BaseModel):
    id: int
    name: str
    projectName: Optional[str] = None
    patientId: str
    date: dt_date
    imageCount: int
    projectId: int
    angles: List[Angle]
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        validate_by_name = True



class ReportCreate(BaseModel):
    name: str
    patientId: str
    date: dt_date
    imageCount: int
    projectId: int
    angles: List[Angle]
    notes: Optional[str] = None

class ReportUpdate(BaseModel):
    name: Optional[str] = None
    patientId: Optional[str] = None
    date: Optional[dt_date] = None
    imageCount: Optional[int] = None
    projectId: Optional[int] = None
    angles: Optional[List[Angle]] = None
    notes: Optional[str] = None

