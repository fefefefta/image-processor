import json
from src.redis_client import redis_client
from src.save_image import save_image_to_media, save_image_data
from src.logger import logger
from src.settings import settings
from src.db import init_db


def process_queue():
    init_db()
    logger.info("Служба image_saver запущена и готова к обработке изображений.")

    while True:
        try:
            _, message = redis_client.blpop(settings.image_queue)
            logger.info("Получено сообщение из очереди Redis.")

            data = json.loads(message)

            if "processed_image_bytes" not in data:
                logger.error(
                    f"Ошибка: 'processed_image_bytes' отсутствует в данных сообщения: {data}"
                )
                continue

            image_data = data["image_data"]
            image_bytes = data["processed_image_bytes"].encode("latin-1")
            logger.info(f"Обрабатывается изображение ID: {image_data['id']}")

            image_path = save_image_to_media(image_bytes, image_data["id"])
            save_image_data(image_data, image_path)

            logger.info(f"Изображение ID: {image_data['id']} успешно сохранено.")
        except Exception as e:
            logger.error(f"Ошибка при обработке очереди: {e}", exc_info=True)


if __name__ == "__main__":
    process_queue()
