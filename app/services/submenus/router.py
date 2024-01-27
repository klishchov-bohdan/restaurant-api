from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Submenu
from app.services.submenus.dependencies import valid_submenu_id
from app.services.submenus.schemas import OutSubmenuSchema, CreateSubmenuSchema
from app.services.submenus.service import get_submenus, create_submenu, update_submenu, delete_submenu

router = APIRouter(
    prefix="/menus",
    tags=['Submenus']
)


# TODO
@router.get("/{menu_id}/submenus",
            response_model=list[OutSubmenuSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Submenus',
            summary='Get all submenus')
async def get_all_submenus_in_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    submenus_orm = await get_submenus(menu_id, session)
    submenus = [OutSubmenuSchema.model_validate(submenu_orm) for submenu_orm in submenus_orm]
    return submenus


@router.get("/{menu_id}/submenus/{submenu_id}",
            response_model=OutSubmenuSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Submenu from Menu by id',
            summary='Get submenu by id')
async def get_submenu(submenu: Submenu = Depends(valid_submenu_id)):
    return OutSubmenuSchema.model_validate(submenu)


@router.post("/{menu_id}/submenus",
             response_model=OutSubmenuSchema,
             status_code=status.HTTP_201_CREATED,
             description='Creating and returning new Submenu',
             summary='Create Submenu')
async def create(menu_id: int, submenu: CreateSubmenuSchema, session: AsyncSession = Depends(get_async_session)):
    created_submenu = await create_submenu(menu_id=menu_id, title=submenu.title, description=submenu.description,
                                           session=session)
    return OutSubmenuSchema.model_validate(created_submenu)


@router.patch("/{menu_id}/submenus/{submenu_id}",
              response_model=OutSubmenuSchema,
              status_code=status.HTTP_200_OK,
              description='Updating and returning the Submenu in menu by id',
              summary='Update Submenu')
async def update(new_submenu: CreateSubmenuSchema, submenu: Submenu = Depends(valid_submenu_id),
                 session: AsyncSession = Depends(get_async_session)):
    updated_submenu = await update_submenu(menu_id=submenu.menu_id, submenu_id=submenu.id, title=new_submenu.title,
                                           description=new_submenu.description, session=session)
    return OutSubmenuSchema.model_validate(updated_submenu)


@router.delete("/{menu_id}/submenus/{submenu_id}",
               status_code=status.HTTP_200_OK,
               description='Delete Submenu by id',
               summary='Delete Submenu by id')
async def delete(submenu: Submenu = Depends(valid_submenu_id), session: AsyncSession = Depends(get_async_session)):
    await delete_submenu(menu_id=submenu.menu_id, submenu_id=submenu.id, session=session)
