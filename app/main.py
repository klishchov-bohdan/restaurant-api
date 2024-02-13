from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.redis_conn import aioredis
from app.src import dish_router, menu_router, submenu_router

app = FastAPI(title='restaurant-api')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(menu_router, prefix=settings.api_prefix)
app.include_router(submenu_router, prefix=settings.api_prefix)
app.include_router(dish_router, prefix=settings.api_prefix)


@app.on_event('startup')
async def startup():
    FastAPICache.init(RedisBackend(aioredis), prefix='fastapi-cache')
