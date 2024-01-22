from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, creat_Tablesdb, delete_db
from typing import List
from uuid import UUID
import crud, models
from schemas import MenuCreate, SubmenuCreate, DishCreate, MenuOut, SubmenuOut, DishOut


router = FastAPI()


# --- Меню ---


@router.get("/delDB")
def del_db():
    return delete_db()


@router.get("/creatTablesDB")
def create_dbase():
    creat_Tablesdb()


@router.post("/api/v1/menus", response_model=MenuOut, status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    menu_out = crud.create_menu(db, menu)
    menu_out.submenus_count = 0
    menu_out.dishes_count = 0
    return menu_out


@router.get("/api/v1/menus", response_model=List[MenuOut])
def read_menus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    menus = crud.get_menus(db, skip=skip, limit=limit)
    for menu in menus:
        menu.submenus_count = db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).count()
        menu.dishes_count = db.query(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu.id).count()
    return menus or []


@router.get("/api/v1/menus/{menu_id}", response_model=MenuOut, status_code=200)
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, menu_id)
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    submenus_count = crud.count_submenus(db, menu.id)
    dishes_count = crud.count_dishes_menu(db, menu.id)
    menu_out = MenuOut(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=submenus_count,
        dishes_count=dishes_count,
    )
    return menu_out


@router.patch("/api/v1/menus/{menu_id}", response_model=MenuOut)
def update_menu(menu_id: UUID, menu_update: MenuCreate, db: Session = Depends(get_db)):
    updated_menu = crud.update_menu(db, menu_id, menu_update.dict())
    if updated_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    submenus_count = crud.count_submenus(db, updated_menu.id)
    dishes_count = crud.count_dishes_menu(db, updated_menu.id)
    menu_out = MenuOut(
        id=updated_menu.id,
        title=updated_menu.title,
        description=updated_menu.description,
        submenus_count=submenus_count,
        dishes_count=dishes_count,
    )
    return menu_out


@router.delete("/api/v1/menus/{menu_id}", response_model=dict)
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_menu(db, menu_id)


# --- Подменю ---


@router.post("/api/v1/menus/{menu_id}/submenus/", response_model=SubmenuOut, status_code=201)
def create_submenu(menu_id: UUID, submenu_create: SubmenuCreate, db: Session = Depends(get_db)):
    created_submenu = crud.create_submenu(db, menu_id, submenu_create.dict())
    dishes_count = crud.count_dishes_sub(db, created_submenu.id)
    submenu_out = SubmenuOut(
        id=created_submenu.id,
        title=created_submenu.title,
        description=created_submenu.description,
        dishes_count=dishes_count,
    )
    return submenu_out


@router.get("/api/v1/menus/{menu_id}/submenus/", response_model=List[SubmenuOut])
def read_submenus(menu_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    submenus = crud.get_submenus(db, menu_id, skip=skip, limit=limit)
    submenus_with_counts = []
    for submenu in submenus:
        dishes_count = crud.count_dishes_sub(db, submenu.id)
        submenu_out = SubmenuOut(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dishes_count,
        )
        submenus_with_counts.append(submenu_out)
    return submenus_with_counts


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def read_submenu(submenu_id: UUID, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, submenu_id)
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    dishes_count = crud.count_dishes_sub(db, submenu.id)
    submenu_out = SubmenuOut(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=dishes_count,
    )
    return submenu_out


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuOut)
def update_submenu(submenu_id: UUID, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    updated_submenu = crud.update_submenu(db, submenu_id, submenu)
    dishes_count = crud.count_dishes_sub(db, updated_submenu.id)
    submenu_out = SubmenuOut(
        id=updated_submenu.id,
        title=updated_submenu.title,
        description=updated_submenu.description,
        dishes_count=dishes_count,
    )
    return submenu_out


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=dict)
def delete_submenu(submenu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_submenu(db, submenu_id)


# --- Блюда ---


@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=DishOut, status_code=201)
def create_dish(submenu_id: UUID, dish: DishCreate, db: Session = Depends(get_db)):
    return crud.create_dish(db, dish, submenu_id)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=List[DishOut], status_code=200)
def read_dishes(submenu_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_dishes(db, submenu_id, skip=skip, limit=limit) or []


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishOut)
def read_dish(dish_id: UUID, db: Session = Depends(get_db)):
    dishes = crud.get_dish(db, dish_id)
    if not dishes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return crud.get_dish(db, dish_id)


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishOut)
def update_dish(dish_id: UUID, dish: DishCreate, db: Session = Depends(get_db)):
    return crud.update_dish(db, dish_id, dish)


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=dict)
def delete_dish(dish_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_dish(db, dish_id)