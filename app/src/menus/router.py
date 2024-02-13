from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from app.constants import request_key_builder
from app.dependencies import InvCacheDependency, UOWDependency
from app.exceptions import DataNotFound
from app.src.menus.exeptions import MenuNotFoundError
from app.src.menus.schemas import CreateMenuSchema, OutMenuSchema, OutModifiedSchema
from app.src.menus.service import MenuService

router = APIRouter(
    prefix='/menus',
    tags=['Menus']
)


@router.get('/',
            response_model=list[OutMenuSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Menus',
            summary='Get all menus')
@cache(namespace='menus', key_builder=request_key_builder)
async def get_all_menus(uow: UOWDependency):
    try:
        menus = await MenuService(uow=uow).get_all()
        return [OutMenuSchema.model_validate(menus) for menus in menus]
    except DataNotFound:
        raise MenuNotFoundError()


@router.get('/{menu_id}',
            response_model=OutMenuSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Menu by the id',
            summary='Get menu by id')
@cache(namespace='menus', key_builder=request_key_builder)
async def get_menu(menu_id: int, uow: UOWDependency):
    try:
        menu = await MenuService(uow=uow).get_one(id=menu_id)
        return OutMenuSchema.model_validate(menu)
    except DataNotFound:
        raise MenuNotFoundError()


@router.post('/',
             response_model=OutModifiedSchema,
             status_code=status.HTTP_201_CREATED,
             description='Create and return new Menu',
             summary='Create new Menu')
async def create_menu(menu: CreateMenuSchema, uow: UOWDependency, ic: InvCacheDependency):
    created_menu = await MenuService(uow=uow).create(menu=menu)
    return OutModifiedSchema.model_validate(created_menu)


@router.patch('/{menu_id}',
              response_model=OutModifiedSchema,
              status_code=status.HTTP_200_OK,
              description='Update and return Menu',
              summary='Update Menu')
async def update_menu(menu_id: int, menu: CreateMenuSchema, uow: UOWDependency, ic: InvCacheDependency):
    try:
        updated_menu = await MenuService(uow=uow).update(id=menu_id, menu=menu)
        return OutModifiedSchema.model_validate(updated_menu)
    except DataNotFound:
        raise MenuNotFoundError()


@router.delete('/{menu_id}',
               status_code=status.HTTP_200_OK,
               description='Delete Menu by id',
               summary='Delete Menu by id')
async def delete_menu(menu_id: int, uow: UOWDependency, ic: InvCacheDependency):
    try:
        await MenuService(uow=uow).delete(id=menu_id)
    except DataNotFound:
        raise MenuNotFoundError()
