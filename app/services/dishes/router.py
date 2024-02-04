from fastapi import APIRouter, status

from app.dependencies import UOWDependency
from app.exceptions import DataNotFound
from app.services.dishes.exeptions import DishNotFoundError
from app.services.dishes.schemas import CreateDishSchema, OutDishSchema
from app.services.dishes.service import DishService

router = APIRouter(
    prefix='/menus',
    tags=['Dishes']
)


# TODO
@router.get('/{menu_id}/submenus/{submenu_id}/dishes',
            response_model=list[OutDishSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Dishes',
            summary='Get all dishes')
async def get_all_dishes_in_submenu(menu_id: int, submenu_id: int, uow: UOWDependency):
    try:
        dishes = await DishService(uow=uow).get_all_in_submenu(submenu_id=submenu_id)
        return [OutDishSchema.model_validate(dish) for dish in dishes]
    except DataNotFound:
        raise DishNotFoundError()


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            response_model=OutDishSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Dish from Submenu by id',
            summary='Get dish by id')
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, uow: UOWDependency):
    try:
        dish = await DishService(uow=uow).get_one(id=dish_id)
        return OutDishSchema.model_validate(dish)
    except DataNotFound:
        raise DishNotFoundError()


@router.post('/{menu_id}/submenus/{submenu_id}/dishes',
             response_model=OutDishSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create and return new Dish',
             summary='Create new Dish')
async def create(menu_id: int, submenu_id: int, dish: CreateDishSchema, uow: UOWDependency):
    created_dish = await DishService(uow=uow).create(submenu_id=submenu_id, dish=dish)
    return OutDishSchema.model_validate(created_dish)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
              response_model=OutDishSchema,
              status_code=status.HTTP_200_OK,
              description='Update and return Dish',
              summary='Update Dish')
async def update(menu_id: int, submenu_id: int, dish_id: int, dish: CreateDishSchema, uow: UOWDependency):
    try:
        updated_submenu = await DishService(uow=uow).update(id=dish_id, dish=dish)
        return OutDishSchema.model_validate(updated_submenu)
    except DataNotFound:
        raise DishNotFoundError()


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
               status_code=status.HTTP_200_OK,
               description='Delete Dish by id',
               summary='Delete Dish by id')
async def delete(menu_id: int, submenu_id: int, dish_id: int, uow: UOWDependency):
    try:
        await DishService(uow=uow).delete(id=dish_id)
    except DataNotFound:
        raise DishNotFoundError()
