from app.schemas import DishSchema
from app.services.dishes.schemas import CreateDishSchema
from app.utils.uow import IUnitOfWork


class DishService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_all_in_submenu(self, submenu_id: int) -> list[DishSchema]:
        async with self.uow:
            dishes = await self.uow.dish_repo.find_all(submenu_id=submenu_id)
        return dishes

    async def get_one(self, id: int) -> DishSchema:
        async with self.uow:
            dish = await self.uow.dish_repo.find_one(id=id)
        return dish

    async def create(self, submenu_id: int, dish: CreateDishSchema) -> DishSchema:
        dish_dict = dish.model_dump()
        dish_dict['submenu_id'] = submenu_id
        async with self.uow:
            created_dish = await self.uow.dish_repo.add_one(data=dish_dict)
            await self.uow.commit()
        return created_dish

    async def update(self, id: int, dish: CreateDishSchema) -> DishSchema:
        dish_dict = dish.model_dump()
        async with self.uow:
            updated_dish = await self.uow.dish_repo.edit_one(id=id, data=dish_dict)
            await self.uow.commit()
        return updated_dish

    async def delete(self, id: int) -> int:
        async with self.uow:
            deleted_id = await self.uow.dish_repo.delete_one(id=id)
            await self.uow.commit()
        return deleted_id
