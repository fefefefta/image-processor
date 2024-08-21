import json

from src.image_processor import process_image
from src.logger import logger
from src.redis_client import redis_client
from src.settings import settings


def process_queue():
    while True:
        try:
            _, message = redis_client.blpop(settings.image_queue)
            data = json.loads(message)

            image_data = data["image_data"]
            image_bytes = data["image_bytes"].encode("latin-1")

            processed_image = process_image(image_bytes, image_data["description"])
            # save_image_to_media(processed_image, image_data["id"])

            output_data = {
                "image_data": image_data,
                "processed_image_bytes": processed_image.decode("latin-1"),
                "timestamp": image_data["timestamp"],
            }

            redis_client.rpush(settings.processed_queue, json.dumps(output_data))
            logger.info(f"Processed and enqueued image data: {image_data['id']}")

        except Exception as e:
            logger.error(f"Error processing queue: {e}")


if __name__ == "__main__":
    process_queue()
