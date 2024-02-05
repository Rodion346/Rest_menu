from src.utils.repository import SQLRepository
from src.db.database import get_db
from src.models.models import Dishes, Submenu, Menu
from src.schemas.submenus import SubmenuIn

class SubmenusRepository(SQLRepository):
    model = Submenu

    def read(self, id: str) -> Submenu:
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