from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.services.dishes.schemas import OutDishSchema, CreateDishSchema
from app.services.dishes.service import get_dishes, get_dish_by_id, create_dish, update_dish, delete_dish

router = APIRouter(
    prefix="/menus",
    tags=['Dishes']
)


# TODO
@router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[OutDishSchema])
async def get_all_dishes_in_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    dishes_orm = await get_dishes(submenu_id, session)
    dishes = [OutDishSchema.model_validate(dish_orm) for dish_orm in dishes_orm]
    return dishes


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=OutDishSchema)
async def get_submenu(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    dish_orm = await get_dish_by_id(submenu_id, dish_id, session)
    if not dish_orm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return OutDishSchema.model_validate(dish_orm)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=OutDishSchema,
             status_code=status.HTTP_201_CREATED)
async def create(menu_id: int, submenu_id: int, dish: CreateDishSchema,
                 session: AsyncSession = Depends(get_async_session)):
    created_dish = await create_dish(
        submenu_id=submenu_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
        session=session)
    return OutDishSchema.model_validate(created_dish)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=OutDishSchema,
              status_code=status.HTTP_200_OK)
async def update(menu_id: int, submenu_id: int, dish_id: int, dish: CreateDishSchema,
                 session: AsyncSession = Depends(get_async_session)):
    updated_dish = await update_dish(submenu_id=submenu_id, dish_id=dish_id, title=dish.title,
                                     description=dish.description, price=dish.price, session=session)
    return OutDishSchema.model_validate(updated_dish)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
async def delete(menu_id: int, submenu_id: int, dish_id: int, session: AsyncSession = Depends(get_async_session)):
    await delete_dish(submenu_id=submenu_id, dish_id=dish_id, session=session)
