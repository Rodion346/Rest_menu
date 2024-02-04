from src.utils.repository import SQLRepository
from src.models.models import Dishes
from src.db.database import get_db


class DishesRepository(SQLRepository):
    model = Dishes

    def read(self, id):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            return query

    def create(self, shemas, submenu_id):
        with get_db() as session:
            db_data = self.model(**shemas.dict(), submenu_id=submenu_id)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data