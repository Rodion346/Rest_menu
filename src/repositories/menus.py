from src.utils.repository import SQLRepository
from sqlalchemy import select, func, distinct
from src.db.database import get_db
from fastapi import HTTPException, status
from src.models.models import Dishes, Submenu, Menu
from src.schemas.menus import MenuIn

class MenusRepository(SQLRepository):
    model = Menu

    def read(self, id: str) -> Menu:
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
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
                .select_from(self.model)
                .outerjoin(Submenu, self.model.id == Submenu.menu_id)
                .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
                .group_by(self.model.id)
            )

            result = session.execute(querys).fetchall()
            if result:
                s_count, d_count = result[0][0], result[0][1]
                query.submenus_count = s_count
                query.dishes_count = d_count
            return query

    def create(self, schemas: MenuIn) -> Menu:
        with get_db() as session:
            db_data = self.model(**schemas.dict())
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data

