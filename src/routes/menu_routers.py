from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, func, case, outerjoin, distinct
from uuid import UUID
from src.database import get_db
from src.models import Menu, Submenu, Dishes
import src.shemas as shemas


router = APIRouter(tags=["Menu"])



@router.get("/api/v1/menus")
def read_menus(session: Session = Depends(get_db)):
    query = session.query(Menu).all()
    return query

@router.get("/api/v1/menus/{menu_id}", response_model=shemas.MenuOut)
def read_menu(menu_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Menu).filter(Menu.id == menu_id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )
    querys = (
        select(
            func.count(distinct(Submenu.id)).label('submenus_count'),
            func.count(distinct(Dishes.id)).label('dishes_count'),
        )
        .select_from(Menu)
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
        .group_by(Menu.id)
    )

    result = session.execute(querys).fetchall()
    if result:
        s_count, d_count = result[0][0], result[0][1]
        query.submenus_count = s_count
        query.dishes_count = d_count
    return query

@router.post("/api/v1/menus", response_model=shemas.MenuIn, status_code=201)
def create_menu(menu: shemas.MenuIn, session: Session = Depends(get_db)):
    db_menu = Menu(**menu.dict())
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu

@router.patch("/api/v1/menus/{menu_id}", response_model=shemas.MenuIn, status_code=200)
def update_menu(menu_id: str, menu_update: dict, session: Session = Depends(get_db)):
    query = session.query(Menu).filter(Menu.id == menu_id).first()
    if query:
        for key, value in menu_update.items():
            setattr(query, key, value)
        session.commit()
        session.refresh(query)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return query

@router.delete("/api/v1/menus/{menu_id}", status_code=200)
def delete_menu(menu_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Menu).filter(Menu.id == menu_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Menu and associated submenus deleted"}

