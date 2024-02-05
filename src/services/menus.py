from src.utils.repository import AbstractRepository
from src.schemas.menus import MenuIn
from src.redis_test.redis_manage import RedisTools

class MenusService:
    def __init__(self, menu_repo: AbstractRepository, redis: RedisTools):
        self.menu_repo: AbstractRepository = menu_repo()
        self.redis: RedisTools = redis()

    def read_all(self):
        all_menus_key = 'all_menus'
        cached_menus = self.redis.get_params(key=all_menus_key)
        if cached_menus is not None:
            return cached_menus

        menu_list = self.menu_repo.read_all()
        self.redis.set_params(all_menus_key, menu_list)
        return menu_list

    def read(self, id):
        cached_menu = self.redis.get_params(id)
        if cached_menu is not None:
            return cached_menu

        menu = self.menu_repo.read(id)
        if menu is not None:
            self.redis.set_params(id, menu)
        return menu

    def create(self, menu_in: MenuIn):
        self.redis.invalid('all_menus')
        menu = self.menu_repo.create(menu_in)
        self.redis.set_params(menu.id, menu)
        return menu

    def update(self, id, data):
        all_menus_key = 'all_menus'
        self.redis.invalid(all_menus_key)
        self.redis.invalid(id)
        menu = self.menu_repo.update(id, data)
        return menu

    def delete(self, id):
        self.redis.invalid(id)
        menu = self.menu_repo.delete(id)
        if menu is not None:
            self.redis.invalid(id)
        return menu