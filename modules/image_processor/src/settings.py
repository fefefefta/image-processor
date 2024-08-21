import os


class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    processed_queue: str = os.getenv("PROCESSED_QUEUE", "processed_image_queue")
    image_queue: str = os.getenv("IMAGE_QUEUE", "image_queue")
    media_path: str = os.getenv("MEDIA_PATH", "/app/media/")


settings = Settings()
