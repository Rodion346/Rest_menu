from typing import Any, Sequence
from uuid import UUID

from fastapi import BackgroundTasks

from src.models.models import Submenu
from src.redis.redis_manage import RedisTools
from src.repositories.submenus import SubmenuRepository
from src.schemas.submenus import SubmenuIn


class SubmenusService:
    all_submenus_key: str = 'all_submenus'

    def __init__(self, submenu_repo: SubmenuRepository, redis: RedisTools):
        self.submenu_repo: SubmenuRepository = submenu_repo
        self.redis: RedisTools = redis

    async def read_all(self) -> Sequence[Submenu]:
        resp = await self.redis.get_params(self.all_submenus_key)
        if resp:
            return resp
        submenu_list: Sequence[Submenu] = await self.submenu_repo.read_all()
        await self.redis.set_params(self.all_submenus_key, submenu_list)
        return submenu_list

    async def read(self, id_ent: UUID) -> Any | None:
        resp = await self.redis.get_params(id_ent)
        if resp:
            return resp
        submenu: Any | None = await self.submenu_repo.read(id_ent)
        await self.redis.set_params(id_ent, submenu)
        return submenu

    async def create(self, schemas: SubmenuIn, menu_id, background_tasks: BackgroundTasks) -> Any:
        submenu: Any = await self.submenu_repo.create(schemas, menu_id)
        background_tasks.add_task(self.redis.invalid, self.all_submenus_key)
        return submenu

    async def update(self, id_ent: UUID, schemas: dict, background_tasks: BackgroundTasks) -> Any | None:
        submenu: Any | None = await self.submenu_repo.update(id_ent, schemas)
        background_tasks.add_task(self.redis.invalid, self.all_submenus_key)
        background_tasks.add_task(self.redis.invalid, id_ent)
        return submenu

    async def delete(self, id_ent: UUID, background_tasks: BackgroundTasks) -> dict:
        submenu: Any = await self.submenu_repo.delete(id_ent)
        background_tasks.add_task(self.redis.count, id_ent)
        background_tasks.add_task(self.redis.invalid_submenu, id_ent)
        return submenu
