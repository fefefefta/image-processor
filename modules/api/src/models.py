from sqlalchemy import Column, Integer, String, DateTime, func
from src.database import Base


class ImageRecord(Base):
    __tablename__ = "image_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String, index=True)
    image_path = Column(String)
