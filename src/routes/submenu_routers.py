from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.routes.depence import get_submenus_service
from src.schemas.submenus import SubmenuIn, SubmenuOut
from src.services.submenus import SubmenusService

router = APIRouter(tags=['Submenu'])


@router.get('/api/v1/menus/{menu_id}/submenus', response_model=list[SubmenuOut])
def read_submenus(submenus_service: SubmenusService = Depends(get_submenus_service)) -> list[SubmenuOut]:
    submenus_list: list[SubmenuOut] = submenus_service.read_all()
    return submenus_list


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
def read_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)) -> SubmenuOut | None:
    submenu: SubmenuOut | None = submenus_service.read(submenu_id)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    return submenu


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=201, response_model=SubmenuOut)
def create_submenu(menu_id: UUID, submenu: SubmenuIn, submenus_service: SubmenusService = Depends(get_submenus_service)) -> SubmenuOut:
    submenu_data: SubmenuOut = submenus_service.create(schemas=submenu, menu_id=menu_id)
    return submenu_data


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
def update_submenu(submenu_id: UUID, submenu_update: dict[str, str], submenus_service: SubmenusService = Depends(get_submenus_service)) -> SubmenuOut:
    new_submenu: SubmenuOut = submenus_service.update(id=str(submenu_id), schemas=submenu_update)
    if not new_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return new_submenu


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)) -> dict[str, str]:
    del_submenu: dict[str, str] = submenus_service.delete(submenu_id)
    if not del_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
    return del_submenu
