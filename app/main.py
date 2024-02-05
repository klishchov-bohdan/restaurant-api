from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.config import settings
from app.services import dish_router, menu_router, submenu_router

app = FastAPI()

# origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(menu_router, prefix=settings.api_prefix)
app.include_router(submenu_router, prefix=settings.api_prefix)
app.include_router(dish_router, prefix=settings.api_prefix)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(f'redis://{settings.redis.server}:{settings.redis.port}')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
