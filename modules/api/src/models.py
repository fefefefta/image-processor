import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class ImageRecord(Base):
    __tablename__ = "image_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String, index=True)
    image_path = Column(String)