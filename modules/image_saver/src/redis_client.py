import redis
from src.settings import settings


redis_client = redis.Redis.from_url(settings.redis_url)
