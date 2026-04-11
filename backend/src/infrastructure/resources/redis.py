import redis.asyncio as aioredis

from config import RedisConfig


def new_redis_client(redis_config: RedisConfig) -> aioredis.Redis:
    return aioredis.from_url(redis_config.url, decode_responses=True)
