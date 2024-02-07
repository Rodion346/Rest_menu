from uuid import UUID

from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.submenus import SubmenuRepository
from src.schemas.submenus import SubmenuIn, SubmenuOut


class SubmenusService:
    all_submenus_key: str = 'all_submenus'

    def __init__(self, submenu_repo: SubmenuRepository, redis: RedisTools):
        self.submenu_repo: SubmenuRepository = submenu_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[SubmenuOut]:
        all_submenus_key: str = self.all_submenus_key
        cached_submenus = self.redis.get_params(key=all_submenus_key)
        if cached_submenus:
            return cached_submenus
        else:
            submenu_list: list[SubmenuOut] = self.submenu_repo.read_all()
            self.redis.set_params(all_submenus_key, submenu_list)
            return submenu_list

    def read(self, id: UUID) -> SubmenuOut | None:
        cached_submenu = self.redis.get_params(str(id))
        if cached_submenu:
            return cached_submenu

        submenu = self.submenu_repo.read(str(id))
        if submenu is not None:
            self.redis.set_params(str(id), submenu)
        return submenu

    def create(self, schemas: SubmenuIn, menu_id: UUID) -> SubmenuOut:
        self.read_all()
        submenu: SubmenuOut = self.submenu_repo.create(schemas, str(menu_id))
        self.redis.add_lists(self.all_submenus_key, submenu)
        self.redis.set_params(submenu.id, submenu)
        self.redis.add_count('s', str(menu_id), str(submenu.id))
        return submenu

    def update(self, id: str, schemas: dict) -> SubmenuOut:
        submenu = self.submenu_repo.update(id, schemas)
        if isinstance(submenu, dict):
            submenu = SubmenuOut(**submenu)
        self.redis.set_params(self.all_submenus_key, self.submenu_repo.read_all())
        self.redis.set_params(id, submenu)

        return submenu

    def delete(self, id: UUID) -> dict[str, str]:
        submenu = SubmenuRepository().read(str(id))
        if submenu is not None:
            self.redis.invalid_submenu(str(id), DishesRepository().read_all())
            self.redis.add_count('d', str(submenu.menu_id), id)
            self.redis.invalid_lists(str(id), self.all_submenus_key)
            self.submenu_repo.delete(str(id))
            return {'message': 'Submenu deleted'}
        else:
            return {'message': 'Submenu not found'}
