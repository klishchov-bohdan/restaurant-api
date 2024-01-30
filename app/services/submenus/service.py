from typing import Dict, Any

from sqlalchemy import select, insert, update, delete, func, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.models import Submenu, Dish


async def get_submenus(menu_id: int, session: AsyncSession):
    try:
        stmt = (
            select(Submenu,
                   func.count(distinct(Dish.id)).label('dishes_count'))
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )
        result = await session.execute(stmt)
        return [{
            'id': submenu[0].id,
            'title': submenu[0].title,
            'description': submenu[0].description,
            'menu_id': submenu[0].menu_id,
            'dishes': submenu[0].dishes,
            'dishes_count': submenu[1],
        } for submenu in result.all()]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_submenu_by_id(menu_id: int, submenu_id: int, session: AsyncSession):
    try:
        stmt = (
            select(Submenu,
                   func.count(distinct(Dish.id)).label('dishes_count'))
            .where(Submenu.id == submenu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )
        result = await session.execute(stmt)
        submenu = result.first()
        if submenu is None:
            return
        return {
            'id': submenu[0].id,
            'title': submenu[0].title,
            'description': submenu[0].description,
            'menu_id': submenu[0].menu_id,
            'dishes': submenu[0].dishes,
            'dishes_count': submenu[1],
        }
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def create_submenu(menu_id: int, title: str, description: str, session: AsyncSession) -> dict[str, Any] | None:
    try:
        stmt = (
            insert(Submenu).values(title=title, description=description, menu_id=menu_id).returning(Submenu.id)
        )
        result = await session.execute(stmt)
        submenu = await get_submenu_by_id(menu_id, result.fetchone()[0], session)
        await session.commit()
        return submenu
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_submenu(menu_id: int, submenu_id: int, title: str, description: str, session: AsyncSession) -> dict[
                                                                                                                    str, Any] | None:
    try:
        stmt = (
            update(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id).values(title=title, description=description).returning(Submenu.id)
        )
        result = await session.execute(stmt)
        submenu = await get_submenu_by_id(menu_id, result.fetchone()[0], session)
        await session.commit()
        return submenu
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def delete_submenu(menu_id: int, submenu_id: int, session: AsyncSession):
    try:
        stmt = (
            delete(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id)
        )
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")