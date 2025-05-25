from pydantic import BaseModel
from typing import List, Optional

class Angle(BaseModel):
    name: str
    value: str

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

