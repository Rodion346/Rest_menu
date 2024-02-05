from decimal import Decimal
from uuid import UUID

from src.models.models import Dishes
from src.redis_test.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.schemas.dishes import DishIn, DishOut


class DishesService:
    def __init__(self, dish_repo: DishesRepository, redis: RedisTools):
        self.dish_repo = dish_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[DishOut]:
        all_dishes_key: str = 'all_dishes'
        cached_dishes: list[DishOut] = self.redis.get_params(key=all_dishes_key)
        if cached_dishes is not None:
            return cached_dishes

        dish_list: list[DishOut] = self.dish_repo.read_all()
        for dish in dish_list:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.set_params(all_dishes_key, dish_list)
        return dish_list

    def read(self, id: UUID) -> Dishes | None:
        cached_dish: DishOut | None = self.redis.get_params(id)
        if cached_dish is not None:
            return cached_dish

        dish = self.dish_repo.read(id)
        if dish is not None:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
            self.redis.set_params(id, dish)
        return dish

    def create(self, schemas: DishIn, submenu_id: UUID) -> Dishes:
        self.redis.invalid('all_dishes')
        dish = self.dish_repo.create(schemas, submenu_id)
        dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.set_params(dish.id, dish)
        return dish

    def update(self, id: UUID, schemas: dict) -> Dishes:
        all_dishes_key: str = 'all_dishes'
        self.redis.invalid(all_dishes_key)
        self.redis.invalid(id)
        dish = self.dish_repo.update(id, schemas)
        return dish

    def delete(self, id: UUID) -> dict[str, str]:
        dish = self.dish_repo.read(id)
        self.redis.invalid(id)
        if dish is not None and dish.submenu_id is not None:
            self.redis.invalid(dish.submenu_id)
        dish = self.dish_repo.delete(id)
        return dish
