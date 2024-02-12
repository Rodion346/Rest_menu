from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from src.routes.depence import get_menus_service
from src.schemas.menus import MenuIn, MenuOut
from src.services.menus import MenusService

router = APIRouter(tags=['Menu'])


@router.get('/api/v1/menus')
async def read_menus(menus_service: MenusService = Depends(get_menus_service)):
    menus_list = await menus_service.read_all()
    return menus_list


@router.get('/api/v1/menus/{menu_id}', response_model=MenuOut)
async def read_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service)) -> MenuOut:
    menu = await menus_service.read(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return menu


@router.post('/api/v1/menus', status_code=201, response_model=MenuOut)
async def create_menu(menu: MenuIn, menus_service: MenusService = Depends(get_menus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuOut:
    menu_data: MenuOut = await menus_service.create(menu, background_tasks)
    return menu_data


@router.patch('/api/v1/menus/{menu_id}', response_model=MenuOut)
async def update_menu(menu_id: UUID, menu_update: dict, menus_service: MenusService = Depends(get_menus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuOut:
    new_menu = await menus_service.update(menu_id, menu_update, background_tasks)
    if not new_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return new_menu


@router.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    del_menu = await menus_service.delete(menu_id, background_tasks)
    if not del_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return del_menu


@router.get('/all')
async def all_dep(menus_service: MenusService = Depends(get_menus_service)):
    dep = await menus_service.all_dep()
    return dep
