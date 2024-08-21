from datetime import datetime
from typing import Annotated, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import ImageRecord
from src.schemas import ImageData, ImageResponse
from src.redis_client import enqueue_image


router = APIRouter()


@router.post("/images", response_model=ImageResponse)
async def upload_image(
    description: str,
    file: Annotated[UploadFile, File(description="The image must be in JPEG format")],
):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Invalid image type")

    image_id = str(uuid4())
    timestamp = datetime.utcnow().isoformat()
    image_data = ImageData(id=image_id, description=description, timestamp=timestamp)

    image_bytes = await file.read()

    enqueue_image(image_data, image_bytes)

    url = f"/images/{image_id}"
    return ImageResponse(
        id=image_id, description=description, timestamp=timestamp, url=url
    )


@router.get("/images", response_model=List[ImageResponse])
async def list_images(db: Session = Depends(get_db)):
    images = db.query(ImageRecord).all()
    return [
        ImageResponse(
            id=str(image.id),
            description=image.description,
            timestamp=image.timestamp,
            url=f"/images/{image.id}",
        )
        for image in images
    ]


@router.get("/images/{id}", response_model=ImageResponse)
async def get_image(id: int, db: Session = Depends(get_db)):
    image = db.query(ImageRecord).filter(ImageRecord.id == id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return ImageResponse(
        id=image.id,
        description=image.description,
        timestamp=image.timestamp,
        url=f"/images/{image.id}",
    )
