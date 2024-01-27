from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import Dish
from app.services.dishes.exeptions import DishNotFoundError
from app.services.dishes.service import get_dish_by_id


async def valid_dish_id(submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)) -> Dish:
    dish = await get_dish_by_id(submenu_id=submenu_id, dish_id=dish_id, session=session)
    if not dish:
        raise DishNotFoundError()
    return dish
