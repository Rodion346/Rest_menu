from src.utils.repository import AbstractRepository
from src.schemas.menus import MenuIn
class MenusService:
    def __init__(self, menu_repo: AbstractRepository):
        self.menu_repo: AbstractRepository = menu_repo()

    def read_all(self):
        menu_list = self.menu_repo.read_all()
        return menu_list

    def read(self, id):
        menu = self.menu_repo.read(id)
        return menu

    def create(self, menu_in: MenuIn):
        menu = self.menu_repo.create(menu_in)
        return menu

    def update(self, id, data):
        menu = self.menu_repo.update(id, data)
        return menu

    def delete(self, id):
        menu = self.menu_repo.delete(id)
        return menu