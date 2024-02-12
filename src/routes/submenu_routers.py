from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from src.routes.depence import get_submenus_service
from src.schemas.submenus import SubmenuIn, SubmenuOut
from src.services.submenus import SubmenusService

router = APIRouter(tags=['Submenu'])


@router.get('/api/v1/menus/{menu_id}/submenus')
async def read_submenus(submenus_service: SubmenusService = Depends(get_submenus_service)):
    submenus_list = await submenus_service.read_all()
    return submenus_list


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def read_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)) -> SubmenuOut:
    submenu = await submenus_service.read(submenu_id)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    return submenu


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=201, response_model=SubmenuOut)
async def create_submenu(menu_id: UUID, submenu: SubmenuIn, submenus_service: SubmenusService = Depends(get_submenus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> SubmenuOut:
    submenu_data = await submenus_service.create(submenu, menu_id, background_tasks)
    return submenu_data


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def update_submenu(submenu_id: UUID, submenu_update: dict, submenus_service: SubmenusService = Depends(get_submenus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> SubmenuOut:
    new_submenu = await submenus_service.update(submenu_id, submenu_update, background_tasks)
    if not new_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return new_submenu


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    del_submenu = await submenus_service.delete(submenu_id, background_tasks)
    if not del_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    return del_submenu
