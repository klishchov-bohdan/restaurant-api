from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.models import Submenu


async def get_submenus(menu_id: int, session: AsyncSession):
    try:
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        result = await session.execute(stmt)
        return [submenu[0] for submenu in result.all()]

    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_submenu_by_id(menu_id: int, submenu_id: int, session: AsyncSession):
    try:
        stmt = (
            select(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id)
        )
        result = await session.execute(stmt)
        first = result.first()
        if first is None:
            return
        submenu = first.Submenu
        return submenu
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def create_submenu(menu_id: int, title: str, description: str, session: AsyncSession) -> Submenu:
    try:
        stmt = (
            insert(Submenu).values(title=title, description=description, menu_id=menu_id).returning(Submenu)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_submenu(menu_id: int, submenu_id: int, title: str, description: str, session: AsyncSession) -> Submenu:
    try:
        stmt = (
            update(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id).values(title=title, description=description).returning(Submenu)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
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