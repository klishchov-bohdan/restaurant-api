import asyncio
from typing import AsyncGenerator, Final

import pytest
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from redis import asyncio as aioredis
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.database import metadata
from app.dependencies import get_uow
from app.main import app
from app.utils.uow import UnitOfWork

_SQLALCHEMY_DATABASE_URL_TEST: Final[
    str] = f'postgresql+asyncpg://{settings.postgres_test.user}:{settings.postgres_test.password}' \
           f'@{settings.postgres_test.host}:{settings.postgres_test.port}/{settings.postgres_test.db}'

engine_test: Final[AsyncEngine] = create_async_engine(_SQLALCHEMY_DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker_test: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(
    engine_test, expire_on_commit=False, autoflush=False, autocommit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


def override_get_uow():
    return UnitOfWork(session_maker=async_session_maker_test)


app.dependency_overrides[get_uow] = override_get_uow


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    redis = aioredis.from_url(f'redis://{settings.redis.server}:{settings.redis.port}')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)  # TODO: careate tables if they are not exists
        await conn.execute(text("insert into menu (title, description) values ('title1', 'description1')"))
        await conn.execute(
            text("insert into submenu (title, description, menu_id) values ('title1', 'description1', 1)"))
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        # await conn.execute(text("truncate menu cascade"))


# event loop create in pytest_asyncio/plugin.py:749:
@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='session')
async def api() -> FastAPI:
    return app
