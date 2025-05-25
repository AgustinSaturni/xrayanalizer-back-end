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
    name: Optional[str]
    patientId: Optional[str]
    description: Optional[str]
    date: Optional[str]
    imageCount: Optional[int]
    reportCount: Optional[int]
