from src.utils.repository import SQLRepository
from src.models.models import Dishes
from src.db.database import get_db
from src.schemas.dishes import DishIn

class DishesRepository(SQLRepository):
    model = Dishes

    def read(self, id) -> Dishes:
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            return query

    def create(self, schemas: DishIn, submenu_id: str) -> Dishes:
        with get_db() as session:
            db_data = self.model(**schemas.dict(), submenu_id=submenu_id)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data