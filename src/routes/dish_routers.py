from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from src.routes.depence import get_dishes_service
from src.schemas.dishes import DishIn, DishOut
from src.services.dishes import DishesService

router = APIRouter(tags=['Dish'])


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=200)
async def read_dishes(dishes_service: DishesService = Depends(get_dishes_service)):
    dishes_list = await dishes_service.read_all()
    return dishes_list


@router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200, response_model=DishOut)
async def read_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service)):
    dish: DishOut | None = await dishes_service.read(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
    else:
        return dish


@router.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201, response_model=DishOut)
async def create_dish(submenu_id: UUID, dish: DishIn, dishes_service: DishesService = Depends(get_dishes_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> DishOut:
    dish_data: DishOut = await dishes_service.create(dish, submenu_id, background_tasks)
    return dish_data


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200, response_model=DishOut)
async def update_dish(dish_id: UUID, dish_update: dict, dishes_service: DishesService = Depends(get_dishes_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> DishOut:
    new_dish: DishOut | None = await dishes_service.update(dish_id, dish_update, background_tasks)
    if not new_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    else:
        return new_dish


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=200)
async def delete_dish(dish_id: UUID, dishes_service: DishesService = Depends(get_dishes_service), background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    del_dish: dict[str, str] = await dishes_service.delete(dish_id, background_tasks)
    if not del_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    return del_dish
