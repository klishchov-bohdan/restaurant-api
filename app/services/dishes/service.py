from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from decimal import Decimal, getcontext

from app.models import Dish


async def get_dishes(submenu_id: int, session: AsyncSession) -> list[Dish]:
    try:
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        result = await session.execute(stmt)
        return [dish[0] for dish in result.all()]

    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def get_dish_by_id(submenu_id: int, dish_id: int, session: AsyncSession) -> Optional[Dish]:
    try:
        stmt = (
            select(Dish).where(Dish.submenu_id == submenu_id).where(
                Dish.id == dish_id)
        )
        result = await session.execute(stmt)
        first = result.first()
        if first is None:
            return
        dish = first.Dish
        return dish
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def create_dish(submenu_id: int, title: str, description: str, price: Decimal, session: AsyncSession) -> Dish:
    try:
        price = round(price, 2)
        stmt = (
            insert(Dish).values(title=title, description=description, submenu_id=submenu_id, price=price).returning(Dish)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_dish(submenu_id: int, dish_id: int, title: str, description: str,
                      price: Decimal, session: AsyncSession) -> Dish:
    try:
        price = round(price, 2)
        stmt = (
            update(Dish)
            .where(Dish.submenu_id == submenu_id)
            .where(Dish.id == dish_id)
            .values(title=title, description=description, price=price).returning(Dish)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.fetchone()[0]
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def delete_dish(submenu_id: int, dish_id, session: AsyncSession):
    try:
        stmt = (
            delete(Dish)
            .where(Dish.submenu_id == submenu_id)
            .where(Dish.id == dish_id)
        )
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
