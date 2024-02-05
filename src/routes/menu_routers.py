from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.menus import MenuIn, MenuOut
from uuid import UUID
from src.routes.depence import get_menus_service
from src.services.menus import MenusService

router = APIRouter(tags=["Menu"])

@router.get('/api/v1/menus')
def read_menus(menus_service: MenusService = Depends(get_menus_service)):
    menus_list = menus_service.read_all()
    return menus_list

@router.get('/api/v1/menus/{menu_id}', response_model=MenuOut)
def read_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service)):
    menu = menus_service.read(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return menu

@router.post('/api/v1/menus', status_code=201, response_model=MenuOut)
def create_menu(menu: MenuIn, menus_service: MenusService = Depends(get_menus_service)):
    menu_data = menus_service.create(menu)
    return menu_data

@router.patch('/api/v1/menus/{menu_id}', response_model=MenuOut)
def update_menu(menu_id: UUID, menu_update: dict, menus_service: MenusService = Depends(get_menus_service)):
    new_menu = menus_service.update(menu_id, menu_update)
    if not new_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return new_menu

@router.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service)):
    del_menu = menus_service.delete(menu_id)
    return del_menu