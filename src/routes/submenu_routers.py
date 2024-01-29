from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from src.database import get_db
from src.models import Submenu, Dishes
import src.shemas as shemas
router = APIRouter(tags=["Submenu"])

@router.get("/api/v1/menus/{menu_id}/submenus")
def read_submenus(menu_id: UUID, session: Session = Depends(get_db)):
    submenus = session.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    return submenus

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=shemas.SubmenuOut)
def read_submenu(menu_id: UUID, submenu_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )
    d_count = session.query(Dishes).join(Submenu).filter(Submenu.menu_id == menu_id).count()
    query.dishes_count = d_count
    return query

@router.post("/api/v1/menus/{menu_id}/submenus", response_model=shemas.SubmenuIn, status_code=201)
def create_submenu(menu_id: UUID, submenu: shemas.SubmenuIn, session: Session = Depends(get_db)):
    query = Submenu(**submenu.dict(), menu_id=menu_id)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=shemas.SubmenuOut)
def update_submenu(submenu_id: UUID, submenu_update: dict, session: Session = Depends(get_db)):
    query = session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if query:
        for key, value in submenu_update.items():
            setattr(query, key, value)
        session.commit()
        session.refresh(query)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return query

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200)
def delete_submenu(submenu_id: UUID, session: Session = Depends(get_db)):
    query = session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Submenu and associated submenus deleted"}

