from db.database import Base  # ✅ La correcta
from pydantic import BaseModel
from datetime import date, datetime
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, String

class ImageORM(Base):
    __tablename__ = "imagen"

    id = Column(BigInteger, primary_key=True, index=True)
    projectId = Column(BigInteger, ForeignKey("proyecto.id"), nullable=False)
    name = Column(String)
    url = Column(String)
    size = Column(Integer)
    uploadedDate = Column(Date)
    # Relación con Proyecto
    project = relationship("ProjectORM", back_populates="images")

class ImageCreate(BaseModel):
    projectId: int
    name: str
    url: str
    size: int
    uploadedDate: date

class Image(BaseModel):
    id: int
    projectId: int
    name: str
    url: str
    size: int
    uploadedDate: datetime

    class Config:
        from_attributes = True
        validate_by_name = True

