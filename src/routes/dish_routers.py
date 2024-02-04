from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from src.repositories.dishes import DishesRepository
from src.services.dishes import DishesService
from src.schemas.dishes import DishIn, DishOut


router = APIRouter(tags=["Dish"])



@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=200)
def read_dishes():
    dishes_list = DishesService(DishesRepository).read_all()
    return dishes_list


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishOut)
def read_dish(dish_id: UUID):
    dish = DishesService(DishesRepository).read(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    else:
        return dish


@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201, response_model=DishOut)
def create_dish(submenu_id: UUID, dish: DishIn):
    dish_data = DishesService(DishesRepository).create(dish, submenu_id, )
    return dish_data

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200, response_model=DishOut)
def update_dish(dish_id: UUID, dish_update: dict):
    new_dish = DishesService(DishesRepository).update(dish_id, dish_update)
    if new_dish == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    else:
        return new_dish

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200)
def delete_dish(dish_id: UUID):
    del_dish = DishesService(DishesRepository).delete(dish_id,)
    return del_dish