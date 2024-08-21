import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    postgres_user: str = os.getenv("POSTGRES_USER", "user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    postgres_db: str = os.getenv("POSTGRES_DB", "image_db")
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    image_queue: str = os.getenv("IMAGE_QUEUE", "processed_image_queue")
    media_path: str = os.getenv("MEDIA_PATH", "/media/")


settings = Settings()
