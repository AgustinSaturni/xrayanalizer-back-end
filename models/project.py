# models/project.py
from sqlalchemy import Column, Integer, String, Date
from db.database import Base
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date as dt_date
from sqlalchemy.orm import relationship


class ProjectORM(Base):
    __tablename__ = "proyecto"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    patientId = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    imageCount = Column(Integer, default=0)
    reportCount = Column(Integer, default=0)

    reports = relationship("ReportORM", back_populates="project",cascade="all, delete-orphan")
    images = relationship("ImageORM", back_populates="project", cascade="all, delete")


class ProjectCreate(BaseModel):
    name: str
    patientId: str
    description: str

class Project(BaseModel):
    id: int
    name: str
    patientId: str
    description: str
    date: dt_date
    reportCount: int
    imageCount: int

    class Config:
        from_attributes = True
        validate_by_name = True


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    patientId: Optional[str] = None
    description: Optional[str] = None
    date: Optional[dt_date] = None
    imageCount: Optional[int] = None
    reportCount: Optional[int] = None
