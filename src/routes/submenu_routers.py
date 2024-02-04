from fastapi import APIRouter, HTTPException, status
from src.repositories.submenus import SubmenusRepository
from src.services.submenus import SubmenusService
from src.schemas.submenus import SubmenuIn, SubmenuOut
from uuid import UUID


router = APIRouter(tags=["Submenu"])

@router.get("/api/v1/menus/{menu_id}/submenus")
def read_submenus():
    submenus_list = SubmenusService(SubmenusRepository).read_all()
    return submenus_list

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def read_submenu(submenu_id: UUID):
    submenu = SubmenusService(SubmenusRepository).read(submenu_id)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    else:
        return submenu

@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201, response_model=SubmenuIn)
def create_submenu(submenu: SubmenuIn, menu_id: UUID):
    submenu_data = SubmenusService(SubmenusRepository).create(submenu, menu_id, )
    return submenu_data

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def update_submenu(submenu_id: UUID, submenu_update: dict):
    new_submenu = SubmenusService(SubmenusRepository).update(submenu_id, submenu_update)
    if new_submenu == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    else:
        return new_submenu

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(submenu_id: UUID):
    del_submenu = SubmenusService(SubmenusRepository).delete(submenu_id, )
    return del_submenu
