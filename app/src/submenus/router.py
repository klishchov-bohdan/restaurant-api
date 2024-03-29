from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from app.constants import request_key_builder
from app.dependencies import InvCacheDependency, UOWDependency
from app.exceptions import DataNotFound
from app.src.submenus.exeptions import SubmenuNotFoundError
from app.src.submenus.schemas import (
    CreateSubmenuSchema,
    OutModifiedSchema,
    OutSubmenuSchema,
)
from app.src.submenus.service import SubmenuService

router = APIRouter(
    prefix='/menus',
    tags=['Submenus']
)


@router.get('/{menu_id}/submenus/',
            response_model=list[OutSubmenuSchema],
            status_code=status.HTTP_200_OK,
            description='Returning the list of the Submenus',
            summary='Get all submenus')
@cache(namespace='submenus', key_builder=request_key_builder)
async def get_all_submenus_in_menu(menu_id: int, uow: UOWDependency):
    try:
        submenus = await SubmenuService(uow=uow).get_all_in_menu(menu_id=menu_id)
        return [OutSubmenuSchema.model_validate(submenu) for submenu in submenus]
    except DataNotFound:
        raise SubmenuNotFoundError()


@router.get('/{menu_id}/submenus/{submenu_id}',
            response_model=OutSubmenuSchema,
            status_code=status.HTTP_200_OK,
            description='Returning the Submenu from Menu by id',
            summary='Get submenu by id')
@cache(namespace='submenus', key_builder=request_key_builder)
async def get_submenu(menu_id: int, submenu_id: int, uow: UOWDependency):
    try:
        submenu = await SubmenuService(uow=uow).get_one(id=submenu_id)
        return OutSubmenuSchema.model_validate(submenu)
    except DataNotFound:
        raise SubmenuNotFoundError()


@router.post('/{menu_id}/submenus/',
             response_model=OutModifiedSchema,
             status_code=status.HTTP_201_CREATED,
             description='Creating and returning new Submenu',
             summary='Create Submenu')
async def create_submenu(menu_id: int, submenu: CreateSubmenuSchema, uow: UOWDependency, ic: InvCacheDependency):
    created_submenu = await SubmenuService(uow=uow).create(menu_id=menu_id, submenu=submenu)
    return OutModifiedSchema.model_validate(created_submenu)


@router.patch('/{menu_id}/submenus/{submenu_id}',
              response_model=OutModifiedSchema,
              status_code=status.HTTP_200_OK,
              description='Updating and returning the Submenu in menu by id',
              summary='Update Submenu')
async def update_submenu(menu_id: int, submenu_id: int, submenu: CreateSubmenuSchema, uow: UOWDependency, ic: InvCacheDependency):
    try:
        updated_submenu = await SubmenuService(uow=uow).update(id=submenu_id, submenu=submenu)
        return OutModifiedSchema.model_validate(updated_submenu)
    except DataNotFound:
        raise SubmenuNotFoundError()


@router.delete('/{menu_id}/submenus/{submenu_id}',
               status_code=status.HTTP_200_OK,
               description='Delete Submenu by id',
               summary='Delete Submenu by id')
async def delete_submenu(menu_id: int, submenu_id: int, uow: UOWDependency, ic: InvCacheDependency):
    try:
        await SubmenuService(uow=uow).delete(id=submenu_id)
    except DataNotFound:
        raise SubmenuNotFoundError()
