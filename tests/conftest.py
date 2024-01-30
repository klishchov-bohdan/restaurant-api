from typing import Final, AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.database import metadata, get_async_session
from app.main import app

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

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
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
# @pytest.fixture(scope='session')
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/api/v1") as async_client:
        yield async_client

