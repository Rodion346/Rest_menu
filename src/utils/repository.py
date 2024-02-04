from abc import ABC, abstractmethod
from src.db.database import get_db

class AbstractRepository(ABC):
    @abstractmethod
    def read_all(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

class SQLRepository(AbstractRepository):
    model = None

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
                return {"message": "Menu and associated submenus deleted"}

