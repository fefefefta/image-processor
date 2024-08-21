import json

import redis

from src.settings import settings
from src.logger import logger


redis_client = redis.Redis.from_url(settings.redis_url)


def enqueue_image(image_data, image_bytes):
    try:
        data = {
            "image_data": image_data.dict(),
            "image_bytes": image_bytes.decode("latin-1"),
        }
        redis_client.rpush("image_queue", json.dumps(data))
        logger.info(f"Enqueued image data: {image_data.id}")
    except Exception as e:
        logger.error(f"Failed to enqueue image data: {e}")
        raise
