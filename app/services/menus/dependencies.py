from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import Menu
from app.services.menus.exeptions import MenuNotFoundError
from app.services.menus.service import get_menu_by_id


async def valid_menu_id(menu_id: int, session: AsyncSession = Depends(get_async_session)) -> Menu:
    menu = await get_menu_by_id(menu_id=menu_id, session=session)
    if not menu:
        raise MenuNotFoundError()
    return menu
