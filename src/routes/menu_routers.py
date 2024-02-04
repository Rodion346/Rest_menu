from fastapi import APIRouter, HTTPException, status
from src.schemas.menus import MenuIn, MenuOut
from uuid import UUID
from src.repositories.menus import MenusRepository
from src.services.menus import MenusService


router = APIRouter(tags=["Menu"])




@router.get("/api/v1/menus")
def read_menus():
    menus_list = MenusService(MenusRepository).read_all()
    return menus_list


@router.get("/api/v1/menus/{menu_id}", response_model=MenuOut)
def read_menu(menu_id: UUID):
        menu = MenusService(MenusRepository).read(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
        return menu


@router.post("/api/v1/menus", status_code=201, response_model=MenuOut)
def create_menu(menu: MenuIn):
    menu_data = MenusService(MenusRepository).create(menu, )
    return menu_data

@router.patch("/api/v1/menus/{menu_id}", response_model=MenuOut)
def update_menu(menu_id: UUID, menu_update: dict):
    new_menu = MenusService(MenusRepository).update(menu_id, menu_update)
    if not new_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return new_menu


@router.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: UUID):
    del_menu = MenusService(MenusRepository).delete(menu_id, )
    return del_menu