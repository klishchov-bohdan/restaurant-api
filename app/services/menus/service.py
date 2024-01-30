from typing import Optional, List, Dict, Any

from sqlalchemy import select, insert, update, delete, func, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.models import Menu, Submenu, Dish


async def get_menus(session: AsyncSession) -> list[dict[str, Any]]:
    try:
        stmt = (
            select(Menu,
                   func.count(distinct(Submenu.id)).label('submenu_count'),
                   func.count(distinct(Dish.id)).label('dish_count'))
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )
        result = await session.execute(stmt)
        return [{
            'id': menu[0].id,
            'title': menu[0].title,
            'description': menu[0].description,
            'submenus': menu[0].submenus,
            'submenus_count': menu[1],
            'dishes_count': menu[2],
        } for menu in result.all()]
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_menu_by_id(menu_id: int, session: AsyncSession) -> dict[str, Any] | None:
    try:
        stmt = (
            select(Menu,
                   func.count(distinct(Submenu.id)).label('submenu_count'),
                   func.count(distinct(Dish.id)).label('dish_count'))
            .where(Menu.id == menu_id)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )
        result = await session.execute(stmt)
        menu = result.first()
        if menu is None:
            return
        return {
            'id': menu[0].id,
            'title': menu[0].title,
            'description': menu[0].description,
            'submenus': menu[0].submenus,
            'submenus_count': menu[1],
            'dishes_count': menu[2],
        }
    except SQLAlchemyError as ex:
        print(ex)
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
