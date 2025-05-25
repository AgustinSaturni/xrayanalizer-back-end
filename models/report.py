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
    projectId: Optional[str]
    projectName: Optional[str]
    patientId: Optional[str]
    name: Optional[str]
    imageCount: Optional[int]
    angles: Optional[List[Angle]]
    notes: Optional[str]
