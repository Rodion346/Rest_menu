from uuid import UUID

from src.models.models import Menu
from src.redis_test.redis_manage import RedisTools
from src.repositories.menus import MenusRepository
from src.schemas.menus import MenuIn


class MenusService:
    def __init__(self, menu_repo: MenusRepository, redis: RedisTools):
        self.menu_repo = menu_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[MenuIn]:
        all_menus_key: str = 'all_menus'
        cached_menus: list[MenuIn] = self.redis.get_params(key=all_menus_key)
        if cached_menus is not None:
            return cached_menus

        menu_list: list[MenuIn] = self.menu_repo.read_all()
        self.redis.set_params(all_menus_key, menu_list)
        return menu_list

    def read(self, id) -> Menu | None:
        cached_menu: MenuIn = self.redis.get_params(id)
        if cached_menu is not None:
            return cached_menu

        menu: MenuIn = self.menu_repo.read(id)
        if menu is not None:
            self.redis.set_params(id, menu)
        return menu

    def create(self, schemas: MenuIn) -> Menu:
        self.redis.invalid('all_menus')
        menu: MenuIn = self.menu_repo.create(schemas)
        self.redis.set_params(menu.id, menu)
        return menu

    def update(self, id: UUID, schemas: dict) -> Menu:
        all_menus_key: str = 'all_menus'
        self.redis.invalid(all_menus_key)
        self.redis.invalid(id)
        menu: MenuIn = self.menu_repo.update(id, schemas)
        return menu

    def delete(self, id: UUID) -> dict[str, str]:
        self.redis.invalid(id)
        menu: MenuIn = self.menu_repo.delete(id)
        if menu is not None:
            self.redis.invalid(id)
        return menu
