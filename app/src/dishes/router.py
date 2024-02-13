from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from app.constants import request_key_builder
from app.dependencies import InvCacheDependency, UOWDependency
from app.exceptions import DataNotFound
from app.src.dishes.exeptions import DishNotFoundError
from app.src.dishes.schemas import CreateDishSchema, OutDishSchema
from app.src.dishes.service import DishService

router = APIRouter(
    prefix='/menus',
    tags=['Dishes']
)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/',
            response_model=list[OutDishSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Dishes',
            summary='Get all dishes',
            responses={
                status.HTTP_200_OK: {
                    'model': list[OutDishSchema],
                    'description': 'Ok Response',
                },
            })
@cache(namespace='dishes', key_builder=request_key_builder)
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
            summary='Get dish by id',
            responses={
                status.HTTP_200_OK: {
                    'model': list[OutDishSchema],
                    'description': 'Ok Response',
                },
                status.HTTP_404_NOT_FOUND: {
                    'model': dict[str, str],
                    'description': 'dish id not exists',
                },
            })
@cache(namespace='dishes', key_builder=request_key_builder)
async def get_dish(menu_id: int, submenu_id: int, dish_id: int, uow: UOWDependency):
    try:
        dish = await DishService(uow=uow).get_one(id=dish_id)
        return OutDishSchema.model_validate(dish)
    except DataNotFound:
        raise DishNotFoundError()


@router.post('/{menu_id}/submenus/{submenu_id}/dishes/',
             response_model=OutDishSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create and return new Dish',
             summary='Create new Dish',
             responses={
                 status.HTTP_201_CREATED: {
                     'model': list[OutDishSchema],
                     'description': 'Ok Response',
                 },
             })
async def create_dish(menu_id: int, submenu_id: int, dish: CreateDishSchema, uow: UOWDependency, ic: InvCacheDependency):
    created_dish = await DishService(uow=uow).create(submenu_id=submenu_id, dish=dish)
    return OutDishSchema.model_validate(created_dish)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
              response_model=OutDishSchema,
              status_code=status.HTTP_200_OK,
              description='Update and return Dish',
              summary='Update Dish')
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: CreateDishSchema, uow: UOWDependency, ic: InvCacheDependency):
    try:
        updated_submenu = await DishService(uow=uow).update(id=dish_id, dish=dish)
        return OutDishSchema.model_validate(updated_submenu)
    except DataNotFound:
        raise DishNotFoundError()


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
               status_code=status.HTTP_200_OK,
               description='Delete Dish by id',
               summary='Delete Dish by id')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, uow: UOWDependency, ic: InvCacheDependency):
    try:
        await DishService(uow=uow).delete(id=dish_id)
    except DataNotFound:
        raise DishNotFoundError()
