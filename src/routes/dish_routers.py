from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from src.routes.depence import get_dishes_service
from src.services.dishes import DishesService
from src.schemas.dishes import DishIn, DishOut

router = APIRouter(tags=["Dish"])

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=200)
def read_dishes(dishes_service: DishesService = Depends(get_dishes_service)):
    dishes_list = dishes_service.read_all()
    return dishes_list

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishOut)
def read_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service)):
    dish = dishes_service.read(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    else:
        return dish

@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201, response_model=DishOut)
def create_dish(submenu_id: UUID, dish: DishIn, dishes_service: DishesService = Depends(get_dishes_service)):
    dish_data = dishes_service.create(dish, submenu_id)
    return dish_data

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200, response_model=DishOut)
def update_dish(dish_id: UUID, dish_update: dict, dishes_service: DishesService = Depends(get_dishes_service)):
    new_dish = dishes_service.update(dish_id, dish_update)
    if new_dish == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    else:
        return new_dish

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200)
def delete_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service)):
    del_dish = dishes_service.delete(dish_id)
    return del_dish