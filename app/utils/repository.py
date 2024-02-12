from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.dialects.postgresql import insert as insertpg
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import DataNotFound


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    async def add_many(self, data: list[dict]):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        print('here')
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Any = None
    base_returning_model: Any = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def _get_last_inserted_id(self) -> int:
        stmt = select(func.max(self.model.id))
        res = await self.session.execute(stmt)
        return res.unique().scalar_one()

    async def add_one(self, data: dict) -> Any:
        if not data.get('id'):
            last_id = await self._get_last_inserted_id()
            if last_id:
                data['id'] = last_id + 1
        stmt = insert(self.model).values(**data).returning(self.base_returning_model)
        res = await self.session.execute(stmt)
        return res.unique().scalar_one().to_base_schema()

    async def add_many(self, data: list[dict]) -> Any:
        stmt = insertpg(self.model).returning(self.base_returning_model)
        stmt_update = stmt.on_conflict_do_update(
            index_elements=[self.model.id],
            set_={name: value
                  for name, value
                  in stmt.excluded.items()
                  if name != 'id' and name != 'time_created'}
        )
        res = await self.session.scalars(stmt_update, data)
        return [row.to_base_schema() for row in res.unique().all()]

    async def edit_one(self, id: int, data: dict) -> Any:
        try:
            stmt = update(self.model) \
                .values(**data) \
                .filter_by(id=id) \
                .returning(self.base_returning_model)
            res = await self.session.execute(stmt)
            return res.unique().scalar_one().to_base_schema()
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def find_all(self, **filter_by) -> list[Any]:
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return [row[0].to_schema() for row in res.unique().all()]
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def find_one(self, **filter_by) -> Any:
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return res.unique().scalar_one().to_schema()
        except NoResultFound as ex:
            raise DataNotFound(ex)

    async def delete_one(self, id: int) -> int:
        try:
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.unique().scalar_one()
        except NoResultFound as ex:
            raise DataNotFound(ex)
