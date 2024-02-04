from src.utils.repository import AbstractRepository
from src.schemas.submenus import SubmenuIn

class SubmenusService:
    def __init__(self, submenu_repo: AbstractRepository):
        self.submenu_repo: AbstractRepository = submenu_repo()

    def read_all(self):
        submenu_list = self.submenu_repo.read_all()
        return submenu_list

    def read(self, id):
        submenu = self.submenu_repo.read(id)
        return submenu

    def create(self, submenu_in: SubmenuIn, menu_id):
        submenu = self.submenu_repo.create(submenu_in, menu_id)
        return submenu

    def update(self, id, data):
        submenu = self.submenu_repo.update(id, data)
        return submenu

    def delete(self, id):
        submenu = self.submenu_repo.delete(id)
        return submenu