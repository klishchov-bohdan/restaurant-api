from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import Submenu
from app.services.submenus.exeptions import SubmenuNotFoundError
from app.services.submenus.service import get_submenu_by_id


async def valid_submenu_id(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)) -> Submenu:
    submenu = await get_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id, session=session)
    if not submenu:
        raise SubmenuNotFoundError()
    return submenu
