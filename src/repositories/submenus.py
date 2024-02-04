from src.utils.repository import SQLRepository
from src.db.database import get_db
from src.models.models import Dishes, Submenu, Menu

class SubmenusRepository(SQLRepository):
    model = Submenu

    def read(self, id):
        with get_db() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            d_count = session.query(Dishes).join(self.model).filter(self.model.menu_id == Menu.id).count()
            if d_count:
                query.dishes_count = d_count
            return query

    def create(self, shemas, menu_id):
        with get_db() as session:
            db_data = self.model(**shemas.dict(), menu_id=menu_id)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
            return db_data