from typing import Any
from uuid import UUID

from src.db.database import get_db
from src.models.models import Dishes
from src.schemas.dishes import DishIn


class DishesRepository:
    model: type[Dishes] = Dishes

    def read(self, id: UUID) -> Dishes | None:
        with get_db() as session:
            query: Dishes | None = session.query(self.model).filter(self.model.id == id).first()
            return query

    def create(self, schemas: DishIn, submenu_id: UUID) -> Dishes:
        with get_db() as session:
            db_data: Dishes = self.model(**schemas.dict(), submenu_id=submenu_id)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data

    def read_all(self) -> list[Dishes]:
        with get_db() as session:
            query: list[Dishes] = session.query(self.model).all()
            return query

    def update(self, id: UUID, data: dict[str, Any]) -> Dishes | None:
        with get_db() as session:
            query: Dishes | None = session.query(self.model).filter(self.model.id == id).first()
            if query:
                for key, value in data.items():
                    setattr(query, key, value)
                session.commit()
                session.refresh(query)
                return query
            return None

    def delete(self, id: UUID) -> dict[str, str]:
        with get_db() as session:
            query: Dishes | None = session.query(self.model).filter(self.model.id == id).first()
            if query:
                session.delete(query)
                session.commit()
                return {'message': 'Menu and associated submenus deleted'}
            else:
                return {'message': f'No dish found with id {id}'}
