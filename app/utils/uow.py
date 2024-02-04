from abc import ABC, abstractmethod

from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubmenuRepository


class IUnitOfWork(ABC):
    menu_repo: MenuRepository
    submenu_repo: SubmenuRepository
    dish_repo: DishRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self, session_maker):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.menu_repo = MenuRepository(self.session)
        self.submenu_repo = SubmenuRepository(self.session)
        self.dish_repo = DishRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
