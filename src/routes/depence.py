from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenusRepository
from src.services.dishes import DishesService
from src.services.menus import MenusService
from src.redis_test.redis_manage import RedisTools
from src.services.submenus import SubmenusService


def get_menus_service():
    return MenusService(MenusRepository, RedisTools)

def get_submenus_service():
    return SubmenusService(SubmenusRepository, RedisTools)

def get_dishes_service():
    return DishesService(DishesRepository, RedisTools)