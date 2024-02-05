from fastapi import APIRouter, HTTPException, status, Depends
from src.routes.depence import get_submenus_service
from src.services.submenus import SubmenusService
from src.schemas.submenus import SubmenuIn, SubmenuOut
from uuid import UUID


router = APIRouter(tags=["Submenu"])

@router.get("/api/v1/menus/{menu_id}/submenus")
def read_submenus(submenus_service: SubmenusService = Depends(get_submenus_service)):
    submenus_list = submenus_service.read_all()
    return submenus_list

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def read_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)):
    submenu = submenus_service.read(submenu_id)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    else:
        return submenu

@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201, response_model=SubmenuIn)
def create_submenu(submenu: SubmenuIn, menu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)):
    submenu_data = submenus_service.create(submenu, menu_id, )
    return submenu_data

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def update_submenu(submenu_id: UUID, submenu_update: dict, submenus_service: SubmenusService = Depends(get_submenus_service)):
    new_submenu = submenus_service.update(submenu_id, submenu_update)
    if new_submenu == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    else:
        return new_submenu

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(submenu_id: UUID, submenus_service: SubmenusService = Depends(get_submenus_service)):
    del_submenu = submenus_service.delete(submenu_id, )
    return del_submenu
