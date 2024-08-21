import os
from datetime import datetime
from src.models import ImageRecord
from src.db import SessionLocal
from src.logger import logger
from src.settings import settings


def save_image_to_media(image_bytes: bytes, image_id: str) -> str:
    image_path = os.path.join(settings.media_path, f"{image_id}.jpg")
    try:
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        logger.info(f"Изображение сохранено в {image_path}")
    except Exception as e:
        logger.error(
            f"Ошибка при сохранении изображения {image_id}: {e}", exc_info=True
        )
        raise
    return image_path


def save_image_data(image_data, image_path):
    db = SessionLocal()
    try:
        timestamp = datetime.fromisoformat(image_data["timestamp"])
        image_record = ImageRecord(
            timestamp=timestamp,
            description=image_data["description"],
            image_path=image_path,
        )
        db.add(image_record)
        db.commit()
        logger.info(
            f"Данные изображения ID: {image_data['id']} сохранены в базу данных."
        )
    except Exception as e:
        logger.error(
            f"Ошибка при сохранении данных изображения {image_data['id']} в базу данных: {e}",
            exc_info=True,
        )
        raise
    finally:
        db.close()
