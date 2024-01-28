from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from src.database import get_db
from src.models import Menu, Submenu, Dishes
import src.shemas as shemas
router = APIRouter(tags=["Dish"])



@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=200)
def read_dishes(session: Session = Depends(get_db)):
    query = session.query(Dishes).all()
    return query

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200, response_model=shemas.DishOut)
def read_dish(dish_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Dishes).filter(Dishes.id == dish_id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )
    return query

@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201, response_model=shemas.DishIn)
def create_dish(submenu_id: UUID, dish: shemas.DishIn, session: Session = Depends(get_db)):
    query = Dishes(**dish.dict(), submenu_id=submenu_id)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200, response_model=shemas.DishOut)
def update_dish(dish_id: UUID, dish_update: dict, session: Session = Depends(get_db)):
    query = session.query(Dishes).filter(Dishes.id == dish_id).first()
    if query:
        for key, value in dish_update.items():
            setattr(query, key, value)
        session.commit()
        session.refresh(query)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return query

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200)
def delete_dish(dish_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Dishes).filter(Dishes.id == dish_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Dish deleted"}