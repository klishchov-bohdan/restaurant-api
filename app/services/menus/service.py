from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.models import Menu


async def get_menus(session: AsyncSession) -> list[Menu]:
    try:
        # ******************************************
        # *                 RAW SQL                *
        # ******************************************
        # SELECT
        #   (SELECT count(submenu.id) AS count_1
        #     FROM submenu
        #     WHERE submenu.menu_id = menu.id) AS submenus_count,
        #   (SELECT count(dish.id) AS count_2
        #     FROM submenu LEFT OUTER JOIN dish ON submenu.id = dish.submenu_id
        #     WHERE submenu.menu_id = menu.id) AS dishes_count,
        #   menu.id,
        #   menu.title,
        #   menu.description,
        #   menu.time_created,
        #   menu.time_updated
        # FROM menu
        stmt = select(Menu)  # submenus_count and dishes_count calculates like subqueries (show Menu model in app/models.py)
        result = await session.execute(stmt)
        return [menu[0] for menu in result.all()]
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_menu_by_id(menu_id: int, session: AsyncSession) -> Optional[Menu]:
    try:
        stmt = (
            select(Menu).where(Menu.id == menu_id)
        )
        result = await session.execute(stmt)
        first = result.first()
        if first is None:
            return
        menu = first.Menu
        return menu
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def create_menu(title: str, description: str, session: AsyncSession) -> Optional[Menu]:
    try:
        stmt = (
            insert(Menu).values(title=title, description=description).returning(Menu.id)
        )
        result = await session.execute(stmt)
        menu = await get_menu_by_id(result.fetchone()[0], session)
        await session.commit()
        return menu
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_menu(menu_id: int, title: str, description: str, session: AsyncSession) -> Optional[Menu]:
    try:
        stmt = (
            update(Menu).where(Menu.id == menu_id).values(title=title, description=description).returning(Menu.id)
        )
        result = await session.execute(stmt)
        menu = await get_menu_by_id(result.fetchone()[0], session)
        await session.commit()
        return menu
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def delete_menu(menu_id: int, session: AsyncSession):
    try:
        stmt = (
            delete(Menu).where(Menu.id == menu_id)
        )
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
