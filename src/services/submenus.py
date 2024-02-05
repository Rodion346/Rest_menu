from uuid import UUID

from src.models.models import Submenu
from src.redis_test.redis_manage import RedisTools
from src.repositories.submenus import SubmenuRepository
from src.schemas.submenus import SubmenuIn


class SubmenusService:
    def __init__(self, submenu_repo: SubmenuRepository, redis: RedisTools):
        self.submenu_repo = submenu_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[SubmenuIn]:
        all_submenus_key: str = 'all_submenus'
        cached_submenus: list[SubmenuIn] = self.redis.get_params(key=all_submenus_key)
        if cached_submenus is not None:
            return cached_submenus

        submenu_list: list[SubmenuIn] = self.submenu_repo.read_all()
        self.redis.set_params(all_submenus_key, submenu_list)
        return submenu_list

    def read(self, id) -> Submenu | None:
        cached_submenu: SubmenuIn = self.redis.get_params(id)
        if cached_submenu is not None:
            return cached_submenu

        submenu: SubmenuIn = self.submenu_repo.read(id)
        if submenu is not None:
            self.redis.set_params(id, submenu)
        return submenu

    def create(self, schemas: SubmenuIn, menu_id: str) -> Submenu:
        self.redis.invalid(menu_id)
        submenu = self.submenu_repo.create(schemas, menu_id)
        self.redis.set_params(submenu.id, submenu)
        return submenu

    def update(self, id: str, schemas: dict) -> Submenu:
        all_submenus_key: str = 'all_submenus'
        self.redis.invalid(all_submenus_key)
        self.redis.invalid(id)
        submenu = self.submenu_repo.update(id, schemas)
        return submenu

    def delete(self, id: UUID) -> dict[str, str]:
        self.redis.invalid(id)
        submenu = self.submenu_repo.delete(id)
        if submenu is not None:
            self.redis.invalid(id)
        return submenu
