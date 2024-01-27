from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Dish
from app.services.dishes.dependencies import valid_dish_id
from app.services.dishes.schemas import OutDishSchema, CreateDishSchema
from app.services.dishes.service import get_dishes, get_dish_by_id, create_dish, update_dish, delete_dish

router = APIRouter(
    prefix="/menus",
    tags=['Dishes']
)


# TODO
@router.get("/{menu_id}/submenus/{submenu_id}/dishes",
            response_model=list[OutDishSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Dishes',
            summary='Get all dishes')
async def get_all_dishes_in_submenu(menu_id: int, submenu_id: int, session: AsyncSession = Depends(get_async_session)):
    dishes_orm = await get_dishes(submenu_id, session)
    dishes = [OutDishSchema.model_validate(dish_orm) for dish_orm in dishes_orm]
    return dishes


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            response_model=OutDishSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Dish from Submenu by id',
            summary='Get dish by id')
async def get_submenu(dish: Dish = Depends(valid_dish_id)):
    return OutDishSchema.model_validate(dish)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=OutDishSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create and return new Dish',
             summary='Create new Dish')
async def create(menu_id: int, submenu_id: int, dish: CreateDishSchema,
                 session: AsyncSession = Depends(get_async_session)):
    created_dish = await create_dish(
        submenu_id=submenu_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
        session=session)
    return OutDishSchema.model_validate(created_dish)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
              response_model=OutDishSchema,
              status_code=status.HTTP_200_OK,
              description='Update and return Dish',
              summary='Update Dish')
async def update(menu_id: int, new_dish: CreateDishSchema, dish: Dish = Depends(valid_dish_id),
                 session: AsyncSession = Depends(get_async_session)):
    updated_dish = await update_dish(submenu_id=dish.submenu_id, dish_id=dish.id, title=new_dish.title,
                                     description=new_dish.description, price=new_dish.price, session=session)
    return OutDishSchema.model_validate(updated_dish)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
               status_code=status.HTTP_200_OK,
               description='Delete Dish by id',
               summary='Delete Dish by id')
async def delete(menu_id: int, dish: Dish = Depends(valid_dish_id), session: AsyncSession = Depends(get_async_session)):
    await delete_dish(submenu_id=dish.submenu_id, dish_id=dish.id, session=session)
