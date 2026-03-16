import logging
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger("aztu.redis")

_redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            max_connections=20,
        )
        try:
            await _redis_client.ping()
        except Exception as exc:
            logger.error("Redis connection failed: %s", exc)
            _redis_client = None
            raise
    return _redis_client
