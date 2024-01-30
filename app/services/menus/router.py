from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Menu
from app.services.menus.dependencies import valid_menu_id
from app.services.menus.schemas import CreateMenuSchema, OutMenuSchema
from app.services.menus.service import create_menu, get_menu_by_id, get_menus, update_menu, delete_menu

router = APIRouter(
    prefix="/menus",
    tags=['Menus']
)


@router.get("/",
            response_model=list[OutMenuSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Menus',
            summary='Get all menus')
async def get_all_menus(session: AsyncSession = Depends(get_async_session)):
    menus_orm = await get_menus(session)
    menus = [OutMenuSchema.model_validate(menu_orm) for menu_orm in menus_orm]
    return menus


@router.get("/{menu_id}",
            response_model=OutMenuSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Menu by the id',
            summary='Get menu by id')
async def get_menu(menu: Menu = Depends(valid_menu_id)):
    return OutMenuSchema.model_validate(menu)


@router.post("/",
             response_model=OutMenuSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create and return new Menu',
             summary='Create new Menu')
async def create(menu: CreateMenuSchema, session: AsyncSession = Depends(get_async_session)):
    created_menu = await create_menu(title=menu.title, description=menu.description, session=session)
    return OutMenuSchema.model_validate(created_menu)


@router.patch("/{menu_id}",
              response_model=OutMenuSchema,
              status_code=status.HTTP_200_OK,
              description='Update and return Menu',
              summary='Update Menu')
async def update(new_menu: CreateMenuSchema, menu: Menu = Depends(valid_menu_id), session: AsyncSession = Depends(get_async_session)):
    updated_menu = await update_menu(menu_id=menu['id'], title=new_menu.title, description=new_menu.description, session=session)
    return OutMenuSchema.model_validate(updated_menu)


@router.delete("/{menu_id}",
               status_code=status.HTTP_200_OK,
               description='Delete Menu by id',
               summary='Delete Menu by id')
async def delete(menu: Menu = Depends(valid_menu_id), session: AsyncSession = Depends(get_async_session)):
    await delete_menu(menu_id=menu['id'], session=session)

