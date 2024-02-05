from decimal import Decimal

from src.redis_test.redis_manage import RedisTools
from src.utils.repository import AbstractRepository
from src.schemas.dishes import DishIn


class DishesService:
    def __init__(self, dish_repo: AbstractRepository, redis: RedisTools):
        self.dish_repo: AbstractRepository = dish_repo()
        self.redis: RedisTools = redis()

    def read_all(self):
        all_dishes_key = 'all_dishes'
        cached_dishes = self.redis.get_params(key=all_dishes_key)
        if cached_dishes is not None:
            return cached_dishes

        dish_list = self.dish_repo.read_all()
        self.redis.set_params(all_dishes_key, dish_list)
        return dish_list

    def read(self, id):
        cached_dish = self.redis.get_params(id)
        if cached_dish is not None:
            return cached_dish

        dish = self.dish_repo.read(id)
        if dish is not None:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
            self.redis.set_params(id, dish)
        return dish

    def create(self, dish_in: DishIn, submenu_id):
        self.redis.invalid('all_dishes')
        dish = self.dish_repo.create(dish_in, submenu_id)
        dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.set_params(dish.id, dish)
        return dish

    def update(self, id, data):
        all_dishes_key = 'all_dishes'
        self.redis.invalid(all_dishes_key)
        self.redis.invalid(id)
        dish = self.dish_repo.update(id, data)
        return dish

    def delete(self, id):
        dish = self.dish_repo.read(id)
        self.redis.invalid(id)
        if dish is not None and dish.submenu_id is not None:
            self.redis.invalid(dish.submenu_id)
        dish = self.dish_repo.delete(id)
        return dish