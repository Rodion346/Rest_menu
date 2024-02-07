from decimal import Decimal
from uuid import UUID

from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.submenus import SubmenuRepository
from src.schemas.dishes import DishIn, DishOut


class DishesService:
    all_dishes_key: str = 'all_dishes'

    def __init__(self, dish_repo: DishesRepository, redis: RedisTools):
        self.dish_repo: DishesRepository = dish_repo
        self.redis: RedisTools = redis

    def read_all(self) -> list[DishOut]:
        cached_dishes: list[DishOut] | None = self.redis.get_params(key=self.all_dishes_key)
        if cached_dishes:
            return cached_dishes
        else:
            dish_list: list[DishOut] = self.dish_repo.read_all()
            for dish in dish_list:
                dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
            self.redis.set_params(self.all_dishes_key, dish_list)
            return dish_list

    def read(self, id: UUID) -> DishOut | None:
        cached_dish = self.redis.get_params(id)
        if cached_dish is not None:
            dish: DishOut = cached_dish
            return dish
        dish_from_repo = self.dish_repo.read(id)
        if dish_from_repo is not None:
            dish_from_repo.price = str(Decimal(dish_from_repo.price).quantize(Decimal('0.00')))
            self.redis.set_params(id, dish_from_repo)
        return dish_from_repo

    def create(self, schemas: DishIn, submenu_id: UUID) -> DishOut:
        self.read_all()
        dish: DishOut = self.dish_repo.create(schemas, submenu_id)
        dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
        self.redis.add_lists(self.all_dishes_key, dish)
        self.redis.set_params(dish.id, dish)
        sub = SubmenuRepository().read(str(submenu_id))
        if sub is not None:
            self.redis.add_count('d', str(sub.menu_id), str(submenu_id))
        return dish

    def update(self, id: UUID, schemas: dict) -> DishOut:
        dish = self.dish_repo.update(id, schemas)
        if dish:
            dish.price = str(Decimal(dish.price).quantize(Decimal('0.00')))
            self.redis.set_params(self.all_dishes_key, self.dish_repo.read_all())
            self.redis.set_params(id, dish)
            return dish
        return DishOut()

    def delete(self, id: UUID) -> dict[str, str]:
        dish = DishesRepository().read(id)
        if dish is None:
            return {'error': 'Dish not found'}
        submenu_id = dish.submenu_id
        sub = SubmenuRepository().read(submenu_id)
        if sub is None:
            return {'error': 'Submenu not found'}
        self.redis.invalid_lists(id, self.all_dishes_key)
        dish_deleted = self.dish_repo.delete(id)
        self.redis.redis_client.delete(str(id))
        self.redis.add_count('d', str(sub.menu_id), str(submenu_id))
        return dish_deleted
