from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.services.submenus.schemas import OutSubmenuSchema, CreateSubmenuSchema
from app.services.submenus.service import get_submenus, get_submenu_by_id, create_submenu, update_submenu, \
    delete_submenu

router = APIRouter(
    prefix="/menus",
    tags=['Submenus']
)


# TODO
@router.get("/{menu_id}/submenus", response_model=list[OutSubmenuSchema])
async def get_all_submenus_in_menu(menu_id: int, session: AsyncSession = Depends(get_async_session)):
    submenus_orm = await get_submenus(menu_id, session)
    submenus = [OutSubmenuSchema.model_validate(submenu_orm) for submenu_orm in submenus_orm]
    return submenus


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=OutSubmenuSchema)
async def get_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    submenu_orm = await get_submenu_by_id(menu_id, submenu_id, session)
    if not submenu_orm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return OutSubmenuSchema.model_validate(submenu_orm)


@router.post("/{menu_id}/submenus", response_model=OutSubmenuSchema, status_code=status.HTTP_201_CREATED)
async def create(menu_id: int, submenu: CreateSubmenuSchema, session: AsyncSession = Depends(get_async_session)):
    created_submenu = await create_submenu(menu_id=menu_id, title=submenu.title, description=submenu.description,
                                           session=session)
    return OutSubmenuSchema.model_validate(created_submenu)


@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=OutSubmenuSchema, status_code=status.HTTP_200_OK)
async def update(menu_id: int, submenu_id: int, submenu: CreateSubmenuSchema, session: AsyncSession = Depends(get_async_session)):
    updated_submenu = await update_submenu(menu_id=menu_id, submenu_id=submenu_id, title=submenu.title, description=submenu.description, session=session)
    return OutSubmenuSchema.model_validate(updated_submenu)


@router.delete("/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
async def delete(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    await delete_submenu(menu_id=menu_id, submenu_id=submenu_id, session=session)
