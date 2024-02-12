import redis
from redis import asyncio

from app.config import settings

aioredis = asyncio.from_url(f'redis://{settings.redis.server}:{settings.redis.port}')

redis_sync = redis.from_url(f'redis://{settings.redis.server}:{settings.redis.port}')
