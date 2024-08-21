from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class ImageData(BaseModel):
    id: str
    description: str
    timestamp: str


class ImageResponse(BaseModel):
    id: UUID
    description: str
    timestamp: datetime
    url: str
    path: str | None = None
