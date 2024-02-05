from typing import List
from src.utils.repository import AbstractRepository
from src.schemas.submenus import SubmenuIn
from src.redis_test.redis_manage import RedisTools

class SubmenusService:
    def __init__(self, submenu_repo: AbstractRepository, redis: RedisTools):
        self.submenu_repo: AbstractRepository = submenu_repo
        self.redis: RedisTools = redis

    def read_all(self) -> List[SubmenuIn]:
        all_submenus_key: str = 'all_submenus'
        cached_submenus: List[SubmenuIn] = self.redis.get_params(key=all_submenus_key)
        if cached_submenus is not None:
            return cached_submenus

        submenu_list: List[SubmenuIn] = self.submenu_repo.read_all()
        self.redis.set_params(all_submenus_key, submenu_list)
        return submenu_list

    def read(self, id) -> SubmenuIn:
        cached_submenu: SubmenuIn = self.redis.get_params(id)
        if cached_submenu is not None:
            return cached_submenu

        submenu: SubmenuIn = self.submenu_repo.read(id)
        if submenu is not None:
            self.redis.set_params(id, submenu)
        return submenu

    def create(self, submenu_in: SubmenuIn, menu_id) -> SubmenuIn:
        self.redis.invalid(menu_id)
        submenu: SubmenuIn = self.submenu_repo.create(submenu_in, menu_id)
        self.redis.set_params(submenu.id, submenu)
        return submenu

    def update(self, id, data) -> SubmenuIn:
        all_submenus_key: str = 'all_submenus'
        self.redis.invalid(all_submenus_key)
        self.redis.invalid(id)
        submenu: SubmenuIn = self.submenu_repo.update(id, data)
        return submenu

    def delete(self, id) -> SubmenuIn:
        self.redis.invalid(id)
        submenu: SubmenuIn = self.submenu_repo.delete(id)
        if submenu is not None:
            self.redis.invalid(id)
        return submenu