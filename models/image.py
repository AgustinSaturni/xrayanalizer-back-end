from pydantic import BaseModel
from datetime import datetime


class Image(BaseModel):
    id: str
    projectId: str
    name: str
    url: str
    type: str
    size: int
    uploadedAt: datetime

    class Config:
        from_attributes = True
        validate_by_name = True
