from pydantic import BaseModel
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    patientId: str
    description: str

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
