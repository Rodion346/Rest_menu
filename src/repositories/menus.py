from fastapi import HTTPException, status
from sqlalchemy import distinct, func, select

from src.db.database import get_db
from src.models.models import Dishes, Menu, Submenu
from src.schemas.menus import MenuIn


class MenusRepository():
    model: type[Menu] = Menu

    def read(self, id):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found',
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

    def read_all(self):
        with get_db() as session:
            query = session.query(self.model).all()
            return query

    def update(self, id, data):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if query:
                for key, value in data.items():
                    setattr(query, key, value)
                session.commit()
                session.refresh(query)
                return query
            else:
                return []

    def delete(self, id):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if query:
                session.delete(query)
                session.commit()
                return {'message': 'Menu and associated submenus deleted'}
