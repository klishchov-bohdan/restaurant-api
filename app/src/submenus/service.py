from app.schemas import SubmenuSchema
from app.src.submenus.schemas import CreateSubmenuSchema
from app.utils.uow import IUnitOfWork


class SubmenuService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_all_in_menu(self, menu_id: int) -> list[SubmenuSchema]:
        async with self.uow:
            submenus = await self.uow.submenu_repo.find_all(menu_id=menu_id)
        return submenus

    async def get_one(self, id: int) -> SubmenuSchema:
        async with self.uow:
            submenu = await self.uow.submenu_repo.find_one(id=id)
        return submenu

    async def create(self, menu_id: int, submenu: CreateSubmenuSchema) -> SubmenuSchema:
        submenu_dict = submenu.model_dump()
        submenu_dict['menu_id'] = menu_id
        async with self.uow:
            created_submenu = await self.uow.submenu_repo.add_one(data=submenu_dict)
            await self.uow.commit()
        return created_submenu

    async def update(self, id: int, submenu: CreateSubmenuSchema) -> SubmenuSchema:
        submenu_dict = submenu.model_dump()
        async with self.uow:
            updated_submenu = await self.uow.submenu_repo.edit_one(id=id, data=submenu_dict)
            await self.uow.commit()
        return updated_submenu

    async def delete(self, id: int) -> int:
        async with self.uow:
            deleted_id = await self.uow.submenu_repo.delete_one(id=id)
            await self.uow.commit()
        return deleted_id
