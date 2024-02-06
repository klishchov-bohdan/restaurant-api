from typing import Annotated

from fastapi import Depends
from fastapi_cache import FastAPICache
from starlette.requests import Request

from app.config import settings
from app.database import async_session_maker
from app.utils.uow import IUnitOfWork, UnitOfWork


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=async_session_maker)


UOWDependency = Annotated[IUnitOfWork, Depends(get_uow)]


async def invalidate_cache(req: Request) -> None:
    path = req.url.path
    while path != settings.api_prefix:
        if path.split('/')[-1].isdigit():
            await FastAPICache.get_backend().clear(key=path)
        else:
            await FastAPICache.get_backend().clear(key=path + '/')
        path_list = path.split('/')
        path = '/'.join(path_list[0:-1])


InvCacheDependency = Annotated[None, Depends(invalidate_cache)]
