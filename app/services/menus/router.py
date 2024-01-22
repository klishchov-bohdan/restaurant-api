from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import MenuSchema, SubmenuSchema, DishSchema
from app.database import get_async_session
from app.models import Menu
from app.services.menus.schemas import CreateMenuSchema, OutMenuSchema
from app.services.menus.service import create_menu, get_menu_by_id, get_menus, update_menu, delete_menu

router = APIRouter(
    prefix="/menus",
    tags=['Menus']
)


# TODO
@router.get("/", response_model=list[OutMenuSchema])
async def get_all_menus(session: AsyncSession = Depends(get_async_session)):
    menus_orm = await get_menus(session)
    menus = [OutMenuSchema.model_validate(menu_orm) for menu_orm in menus_orm]
    return menus


@router.get("/{menu_id}", response_model=OutMenuSchema)
async def get_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    menu_orm = await get_menu_by_id(menu_id, session)
    if not menu_orm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return OutMenuSchema.model_validate(menu_orm)


@router.post("/", response_model=OutMenuSchema, status_code=status.HTTP_201_CREATED)
async def create(menu: CreateMenuSchema, session: AsyncSession = Depends(get_async_session)):
    created_menu = await create_menu(title=menu.title, description=menu.description, session=session)
    return OutMenuSchema.model_validate(created_menu)


@router.patch("/{menu_id}", response_model=OutMenuSchema, status_code=status.HTTP_200_OK)
async def update(menu_id: int, menu: CreateMenuSchema, session: AsyncSession = Depends(get_async_session)):
    updated_menu = await update_menu(menu_id=menu_id, title=menu.title, description=menu.description, session=session)
    return OutMenuSchema.model_validate(updated_menu)


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK)
async def delete(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    await delete_menu(menu_id=menu_id, session=session)

