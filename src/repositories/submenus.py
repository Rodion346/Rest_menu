from src.db.database import get_db
from src.models.models import Dishes, Menu, Submenu
from src.schemas.submenus import SubmenuIn


class SubmenuRepository:
    model: type[Submenu] = Submenu

    def read(self, id: str) -> Submenu | None:
        with get_db() as session:
            query: Submenu | None = session.query(self.model).filter(self.model.id == id).first()
            if query:
                d_count: int = session.query(Dishes).join(self.model).filter(self.model.menu_id == Menu.id).count()
                query.dishes_count = d_count
            return query

    def create(self, schemas: SubmenuIn, menu_id: str) -> Submenu:
        with get_db() as session:
            db_data: Submenu = self.model(**schemas.dict(), menu_id=menu_id)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data

    def read_all(self) -> list[Submenu]:
        with get_db() as session:
            query: list[Submenu] = session.query(self.model).all()
            return query

    def update(self, id: str, data: dict[str, str]) -> Submenu | dict[str, str]:
        with get_db() as session:
            query: Submenu | None = session.query(self.model).filter(self.model.id == id).first()
            if query:
                for key, value in data.items():
                    setattr(query, key, value)
                session.commit()
                session.refresh(query)
                return query
            else:
                return {}

    def delete(self, id: str) -> dict[str, str]:
        with get_db() as session:
            query: Submenu | None = session.query(self.model).filter(self.model.id == id).first()
            if query:
                session.delete(query)
                session.commit()
                return {'message': 'Menu and associated submenus deleted'}
            else:
                return {'message': f'No submenu found with id {id}'}
