from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.routes.depence import get_dishes_service
from src.schemas.dishes import DishIn, DishOut
from src.services.dishes import DishesService

router = APIRouter(tags=['Dish'])


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=200, response_model=list[DishOut])
def read_dishes(dishes_service: DishesService = Depends(get_dishes_service)) -> list[DishOut]:
    dishes_list: list[DishOut] = dishes_service.read_all()
    return dishes_list


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200, response_model=DishOut)
def read_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service)) -> DishOut:
    dish: DishOut | None = dishes_service.read(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        return dish


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201, response_model=DishOut)
def create_dish(submenu_id: UUID, dish: DishIn, dishes_service: DishesService = Depends(get_dishes_service)) -> DishOut:
    dish_data: DishOut = dishes_service.create(dish, submenu_id)
    return dish_data


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200, response_model=DishOut)
def update_dish(dish_id: UUID, dish_update: dict[str, str], dishes_service: DishesService = Depends(get_dishes_service)) -> DishOut:
    new_dish: DishOut = dishes_service.update(dish_id, dish_update)
    if not new_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    else:
        return new_dish


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200)
def delete_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service)) -> dict[str, str]:
    del_dish: dict[str, str] = dishes_service.delete(dish_id)
    if not del_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return del_dish
