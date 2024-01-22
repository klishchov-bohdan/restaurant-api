from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException

from app.models import Menu


async def get_menus(session: AsyncSession):
    try:
        stmt = select(Menu)
        result = await session.execute(stmt)
        return [menu[0] for menu in result.all()]

    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_menu_by_id(menu_id: int, session: AsyncSession):
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
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def create_menu(title: str, description: str, session: AsyncSession) -> Menu:
    try:
        stmt = (
            insert(Menu).values(title=title, description=description).returning(Menu)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_menu(menu_id: int, title: str, description: str, session: AsyncSession) -> Menu:
    try:
        stmt = (
            update(Menu).where(Menu.id == menu_id).values(title=title, description=description).returning(Menu)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def delete_menu(menu_id: int, session: AsyncSession) -> Menu:
    try:
        stmt = (
            delete(Menu).where(Menu.id == menu_id)
        )
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")