from decimal import Decimal
from typing import Any, Sequence
from uuid import UUID

from fastapi import BackgroundTasks

from src.admin.exel import disc
from src.models.models import Dishes
from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.schemas.dishes import DishIn


class DishesService:
    all_dishes_key: str = 'all_dishes'

    def __init__(self, dish_repo: DishesRepository, redis: RedisTools):
        self.dish_repo: DishesRepository = dish_repo
        self.redis: RedisTools = redis
        self.d = disc()

    async def read_all(self) -> Sequence[Dishes]:
        resp = await self.redis.get_params(self.all_dishes_key)
        if resp:
            return resp
        dish_list: Sequence[Dishes] = await self.dish_repo.read_all()
        await self.redis.set_params(self.all_dishes_key, dish_list)
        return dish_list

    async def read(self, id_ent: UUID) -> Any | None:
        resp = await self.redis.get_params(id_ent)
        if resp:
            return resp
        dish: Any | None = await self.dish_repo.read(id_ent, self.d)
        if dish:
            dish.price = Decimal(dish.price).quantize(Decimal('.01'))
        await self.redis.set_params(id_ent, dish)
        return dish

    async def create(self, schemas: DishIn, submenu_id, background_tasks: BackgroundTasks) -> Any:
        dish: Any = await self.dish_repo.create(schemas, submenu_id)
        background_tasks.add_task(self.redis.invalid, self.all_dishes_key)
        return dish

    async def update(self, id_ent: UUID, schemas, background_tasks: BackgroundTasks) -> Any | None:
        dish: Any | None = await self.dish_repo.update(id_ent, schemas)
        background_tasks.add_task(self.redis.invalid, self.all_dishes_key)
        background_tasks.add_task(self.redis.invalid, id_ent)
        return dish

    async def delete(self, id_ent: UUID, background_tasks: BackgroundTasks) -> dict:
        dish: Any = await self.dish_repo.delete(id_ent)
        background_tasks.add_task(self.redis.invalid, id_ent)
        return dish
