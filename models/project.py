# models/project.py
from sqlalchemy import Column, Integer, String, Date
from db.database import Base
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date

class ProjectORM(Base):
    __tablename__ = "proyecto"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    image_count = Column(Integer, default=0)
    report_count = Column(Integer, default=0)

class ProjectCreate(BaseModel):
    name: str
    patientId: str = Field(..., alias="patient_id")
    description: str

class Project(BaseModel):
    id: int
    name: str
    patient_id: str = Field(..., alias="patientId")
    description: str
    date: date
    image_count: int = Field(..., alias="imageCount")
    report_count: int = Field(..., alias="reportCount")

    class Config:
        orm_mode = True
        populate_by_name = True  # <-- para salida en camelCase
        allow_population_by_field_name = True  # <-- para entrada en camelCase


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    patientId: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    imageCount: Optional[int] = None
    reportCount: Optional[int] = None
