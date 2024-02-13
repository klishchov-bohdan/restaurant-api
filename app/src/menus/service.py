from app.schemas import MenuSchema
from app.src.menus.schemas import CreateMenuSchema
from app.utils.uow import IUnitOfWork


class MenuService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_all(self) -> list[MenuSchema]:
        async with self.uow:
            menus = await self.uow.menu_repo.find_all()
        return menus

    async def get_one(self, id: int) -> MenuSchema:
        async with self.uow:
            menu = await self.uow.menu_repo.find_one(id=id)
        return menu

    async def create(self, menu: CreateMenuSchema) -> MenuSchema:
        menu_dict = menu.model_dump()
        async with self.uow:
            created_menu = await self.uow.menu_repo.add_one(data=menu_dict)
            await self.uow.commit()
        return created_menu

    async def update(self, id: int, menu: CreateMenuSchema) -> MenuSchema:
        menu_dict = menu.model_dump()
        async with self.uow:
            updated_menu = await self.uow.menu_repo.edit_one(id=id, data=menu_dict)
            await self.uow.commit()
        return updated_menu

    async def delete(self, id: int) -> int:
        async with self.uow:
            deleted_id = await self.uow.menu_repo.delete_one(id=id)
            await self.uow.commit()
        return deleted_id
