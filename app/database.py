from typing import AsyncGenerator, Final

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.config import settings

_SQLALCHEMY_DATABASE_URL: Final[str] = f'postgresql+asyncpg://{settings.postgres.user}:{settings.postgres.password}' \
    f'@{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.db}'

engine: Final[AsyncEngine] = create_async_engine(_SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
async_session_maker: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, autocommit=False
)

metadata = MetaData(
    naming_convention={
        'ix': 'ix_%(table_name)s_%(column_0_N_name)s ',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s ',
        'ck': 'ck_%(table_name)s_%(constraint_name)s ',
        'fk': 'fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }
)

Base = declarative_base(metadata=metadata, cls=AsyncAttrs)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
