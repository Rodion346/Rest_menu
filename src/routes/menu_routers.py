from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.routes.depence import get_menus_service
from src.schemas.menus import MenuIn, MenuOut
from src.services.menus import MenusService

router = APIRouter(tags=['Menu'])


@router.get('/api/v1/menus', response_model=list[MenuOut])
def read_menus(menus_service: MenusService = Depends(get_menus_service)) -> list[MenuOut]:
    menus_list: list[MenuOut] = menus_service.read_all()
    return menus_list


@router.get('/api/v1/menus/{menu_id}', response_model=MenuOut)
def read_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service)) -> MenuOut:
    menu: MenuOut | None = menus_service.read(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return menu


@router.post('/api/v1/menus', status_code=201, response_model=MenuOut)
def create_menu(menu: MenuIn, menus_service: MenusService = Depends(get_menus_service)) -> MenuOut:
    menu_data: MenuOut = menus_service.create(menu)
    return menu_data


@router.patch('/api/v1/menus/{menu_id}', response_model=MenuOut)
def update_menu(menu_id: UUID, menu_update: dict[str, str], menus_service: MenusService = Depends(get_menus_service)) -> MenuOut:
    new_menu: MenuOut = menus_service.update(menu_id, menu_update)
    if not new_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return new_menu


@router.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: UUID, menus_service: MenusService = Depends(get_menus_service)) -> dict[str, str]:
    del_menu: dict[str, str] = menus_service.delete(menu_id)
    if not del_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return del_menu
