import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Image Upload API"
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    log_level: str = "INFO"
    postgres_user: str = os.getenv("POSTGRES_USER", "user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    postgres_db: str = os.getenv("POSTGRES_DB", "image_db")
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")


settings = Settings()
