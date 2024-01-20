from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas import MenuCreate, SubmenuCreate, DishCreate


# --- Меню ---

def create_menu(db: Session, menu: MenuCreate):
    db_menu = models.Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menus(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Menu).offset(skip).limit(limit).all()


def count_submenus(db: Session, menu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).count()


def count_dishes_menu(db: Session, menu_id: int):
    return db.query(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu_id).count()


def get_menu(db: Session, menu_id: UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def update_menu(db: Session, menu_id: str, menu_update: dict):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        for key, value in menu_update.items():
            setattr(db_menu, key, value)
        db.commit()
        db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session):
    menu = (db.query(models.Menu).options(joinedload(models.Menu.submenus)).first())
    if menu:
        for submenu in menu.submenus:
            delete_submenu(db, submenu.id)
        db.delete(menu)
        db.commit()
        return {"message": "Menu and associated submenus deleted"}
    return {"message": "Menu not found"}


# --- Подменю ---


def count_dishes_sub(db: Session, submenu_id: int):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).count()


def create_submenu(db: Session, menu_id: UUID, submenu_data: dict):
    db_submenu = models.Submenu(**submenu_data, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_submenus(db: Session, menu_id: int, skip: int = 0, limit: int = 10):
    return (db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).offset(skip).limit(limit).all())


def get_submenu(db: Session, submenu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()


def update_submenu(db: Session, submenu_id: int, submenu: SubmenuCreate):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    for key, value in submenu.dict().items():
        setattr(db_submenu, key, value)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, submenu_id: int):
    submenu = (db.query(models.Submenu).options(joinedload(models.Submenu.dishes)).filter(models.Submenu.id == submenu_id).first())
    if submenu:
        for dish in submenu.dishes:
            db.delete(dish)
        db.delete(submenu)
        db.commit()
        return {"message": "Submenu and associated dishes deleted"}
    return {"message": "Submenu not found"}


# --- Блюда ---


def create_dish(db: Session, dish: DishCreate, submenu_id: int):
    db_dish = models.Dish(**dish.dict(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def get_dishes(db: Session, submenu_id: int, skip: int = 0, limit: int = 10):
    return (db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).offset(skip).limit(limit).all())


def get_dish(db: Session, dish_id: int):
    return db.query(models.Dish).filter(models.Dish.id == dish_id).first()


def update_dish(db: Session, dish_id: int, dish: DishCreate):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    for key, value in dish.dict().items():
        setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, dish_id: int):
    db.query(models.Dish).filter(models.Dish.id == dish_id).delete()
    db.commit()
    return {"message": "Dish deleted"}