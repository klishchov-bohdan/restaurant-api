from typing import Annotated

from fastapi import BackgroundTasks, Depends
from fastapi_cache import FastAPICache
from starlette.requests import Request

from app.config import settings
from app.database import async_session_maker
from app.redis_conn import aioredis
from app.utils.uow import IUnitOfWork, UnitOfWork


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=async_session_maker)


UOWDependency = Annotated[IUnitOfWork, Depends(get_uow)]


async def invalidate_cache(path: str) -> None:
    keys = aioredis.scan_iter(f'{path}*')
    async for key in keys:
        await aioredis.delete(key)
    while path != settings.api_prefix:
        if path.split('/')[-1].isdigit():
            await FastAPICache.get_backend().clear(key=path)
        else:
            await FastAPICache.get_backend().clear(key=path + '/')
        path_list = path.split('/')
        path = '/'.join(path_list[0:-1])


async def run_invalidation_in_background(req: Request, background_tasks: BackgroundTasks) -> None:
    path = req.url.path
    background_tasks.add_task(invalidate_cache, path)


InvCacheDependency = Annotated[None, Depends(run_invalidation_in_background)]
