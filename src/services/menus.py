from typing import Any, Sequence

from fastapi import BackgroundTasks

from src.models.models import Menu
from src.redis.redis_manage import RedisTools
from src.repositories.menus import MenusRepository
from src.schemas.menus import MenuIn


class MenusService:
    all_menus_key: str = 'all_menus'

    def __init__(self, menu_repo: MenusRepository, redis: RedisTools):
        self.menu_repo: MenusRepository = menu_repo
        self.redis: RedisTools = redis

    async def read_all(self) -> Sequence[Menu]:
        resp = await self.redis.get_params(self.all_menus_key)
        if resp:
            return resp
        menu_list: Sequence[Menu] = await self.menu_repo.read_all()
        await self.redis.set_params(self.all_menus_key, menu_list)
        return menu_list

    async def read(self, id_ent) -> Any | None:
        resp = await self.redis.get_params(id_ent)
        if resp:
            return resp
        menu: Any | None = await self.menu_repo.read(id_ent)
        await self.redis.set_params(id_ent, menu)
        return menu

    async def create(self, schemas: MenuIn, background_tasks: BackgroundTasks) -> Any:
        menu: Any = await self.menu_repo.create(schemas)
        background_tasks.add_task(self.redis.invalid, self.all_menus_key)
        return menu

    async def update(self, id_ent, schemas: dict, background_tasks: BackgroundTasks) -> Any | None:
        menu: Any | None = await self.menu_repo.update(id_ent, schemas)
        background_tasks.add_task(self.redis.invalid, self.all_menus_key)
        background_tasks.add_task(self.redis.invalid, id_ent)
        return menu

    async def delete(self, id_ent, background_tasks: BackgroundTasks) -> dict:
        menu: Any = await self.menu_repo.delete(id_ent)
        background_tasks.add_task(self.redis.invalid_menu, id_ent)
        return menu

    async def all_dep(self):
        dep = await self.menu_repo.read_Dep()
        return dep
