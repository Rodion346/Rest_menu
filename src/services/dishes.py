from decimal import Decimal
from typing import List, Optional
from src.redis_test.redis_manage import RedisTools
from src.utils.repository import AbstractRepository
from src.schemas.dishes import DishIn, DishOut


class DishesService:
    def __init__(self, dish_repo: AbstractRepository, redis: RedisTools):
        self.dish_repo: AbstractRepository = dish_repo
        self.redis: RedisTools = redis

    def read_all(self) -> List[DishOut]:
        all_dishes_key: str = 'all_dishes'
        cached_dishes: List[DishOut] = self.redis.get_params(key=all_dishes_key)
        if cached_dishes is not None:
            return cached_dishes

        dish_list: List[DishOut] = self.dish_repo.read_all()
        for dish in dish_list:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.set_params(all_dishes_key, dish_list)
        return dish_list

    def read(self, id) -> Optional[DishOut]:
        cached_dish: Optional[DishOut] = self.redis.get_params(id)
        if cached_dish is not None:
            return cached_dish

        dish: Optional[DishOut] = self.dish_repo.read(id)
        if dish is not None:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
            self.redis.set_params(id, dish)
        return dish

    def create(self, dish_in: DishIn, submenu_id) -> DishOut:
        self.redis.invalid('all_dishes')
        dish: DishOut = self.dish_repo.create(dish_in, submenu_id)
        dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.set_params(dish.id, dish)
        return dish

    def update(self, id, data) -> DishOut:
        all_dishes_key: str = 'all_dishes'
        self.redis.invalid(all_dishes_key)
        self.redis.invalid(id)
        dish: DishOut = self.dish_repo.update(id, data)
        return dish

    def delete(self, id) -> DishOut:
        dish: DishOut = self.dish_repo.read(id)
        self.redis.invalid(id)
        if dish is not None and dish.submenu_id is not None:
            self.redis.invalid(dish.submenu_id)
        dish: DishOut = self.dish_repo.delete(id)
        return dish