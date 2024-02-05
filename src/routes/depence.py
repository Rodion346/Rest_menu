from src.redis_test.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.services.dishes import DishesService
from src.services.menus import MenusService
from src.services.submenus import SubmenusService


def get_menus_service() -> MenusService:
    return MenusService(MenusRepository(), RedisTools())


def get_submenus_service() -> SubmenusService:
    return SubmenusService(SubmenuRepository(), RedisTools())


def get_dishes_service() -> DishesService:
    return DishesService(DishesRepository(), RedisTools())
