from uuid import UUID

from src.models.models import Menu
from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.schemas.menus import MenuIn, MenuOut


class MenusService:
    all_menus_key: str = 'all_menus'

    def __init__(self, menu_repo: MenusRepository, redis: RedisTools):
        self.menu_repo: MenusRepository = menu_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[MenuOut]:
        cached_menus = self.redis.get_params(key=self.all_menus_key)
        if cached_menus is not None:
            return cached_menus
        else:
            menu_list: list[MenuOut] = self.menu_repo.read_all()
            self.redis.set_params(self.all_menus_key, menu_list)
            return menu_list

    def read(self, id: UUID) -> MenuOut | None:
        cached_menu: Menu | None = self.redis.get_params(str(id))
        if cached_menu is not None:
            return cached_menu

        menu: Menu | None = self.menu_repo.read(str(id))
        if menu is not None:
            self.redis.set_params(str(id), menu)
            return menu
        return None

    def create(self, schemas: MenuIn) -> MenuOut:
        self.read_all()
        created_menu: Menu = self.menu_repo.create(schemas)
        self.redis.set_params(created_menu.id, created_menu)
        self.redis.add_lists(self.all_menus_key, created_menu)
        return created_menu

    def update(self, id: UUID, schemas: dict) -> MenuOut:
        menu: Menu | dict[str, str] = self.menu_repo.update(str(id), schemas)
        if isinstance(menu, Menu):
            self.redis.set_params(self.all_menus_key, self.menu_repo.read_all())
            self.redis.set_params(str(id), menu)
            return menu
        else:
            raise Exception('Menu not found or update error')

    def delete(self, id: UUID) -> dict[str, str]:
        self.redis.invalid_lists(id, self.all_menus_key)
        self.redis.invalid_menu(str(id), SubmenuRepository().read_all(), DishesRepository().read_all())
        menu: dict[str, str] = self.menu_repo.delete(str(id))
        return menu
