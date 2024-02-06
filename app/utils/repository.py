from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import DataNotFound


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Any = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_one(self, data: dict) -> Any:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one().to_schema()

    async def edit_one(self, id: int, data: dict) -> Any:
        try:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model)
            res = await self.session.execute(stmt)
            return res.scalar_one().to_schema()
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def find_all(self, **filter_by) -> list[Any]:
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return [row[0].to_schema() for row in res.all()]
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def find_one(self, **filter_by) -> Any:
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return res.scalar_one().to_schema()
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def delete_one(self, id: int) -> int:
        try:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound as ex:
            raise DataNotFound(ex)
