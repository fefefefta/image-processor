from pydantic import BaseModel
from datetime import datetime


class ImageData(BaseModel):
    id: str
    description: str
    timestamp: str


class ImageResponse(BaseModel):
    id: str
    description: str
    timestamp: datetime
    url: str
