from src.db.database import get_db
from src.models.models import Dishes, Menu, Submenu
from src.schemas.submenus import SubmenuIn


class SubmenuRepository():
    model: type[Submenu] = Submenu

    def read(self, id):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            d_count = session.query(Dishes).join(self.model).filter(self.model.menu_id == Menu.id).count()
            if d_count:
                query.dishes_count = d_count
            return query

    def create(self, schemas: SubmenuIn, menu_id: str) -> Submenu:
        with get_db() as session:
            db_data = self.model(**schemas.dict(), menu_id=menu_id)
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
