import asyncio
from contextlib import contextmanager
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.db.database import metadata
from src.models.models import Menu
from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.schemas.dishes import DishIn
from src.schemas.menus import MenuIn
from src.schemas.submenus import SubmenuIn

DATABASE_URL_TEST: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa: E231
engine_test = create_engine(DATABASE_URL_TEST)
metadata.bind = engine_test
sessionmaker_test: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@contextmanager
def override_get_db() -> Generator:
    db: sessionmaker = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session', autouse=True)
def setup_db() -> None:
    with override_get_db() as db:
        assert db.bind.url.database == DB_NAME
        Menu.metadata.drop_all(engine_test)
        Menu.metadata.create_all(engine_test)
        db.commit()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://localhost') as ac:
        yield ac
        await ac.aclose()


@pytest.fixture
async def create_menu(request, menu_data: dict):
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = await menu_repo.create(MenuIn(**menu_data))

    async def fin() -> None:
        await menu_repo.delete(menu.id)
        await RedisTools().redis_client.flushdb()

    yield menu
    await fin()


@pytest.fixture
async def create_submenu(request, menu_data: dict, submenu_data: dict):
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = await menu_repo.create(MenuIn(**menu_data))
    submenu_repo: SubmenuRepository = SubmenuRepository()
    submenu: SubmenuIn = await submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    async def fin() -> None:
        await menu_repo.delete(menu.id)
        await submenu_repo.delete(submenu.id)
        await RedisTools().redis_client.flushdb()

    yield submenu
    await fin()


@pytest.fixture
async def create_dish(request, menu_data: dict, submenu_data: dict, dish_data: dict):
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = await menu_repo.create(MenuIn(**menu_data))

    submenu_repo: SubmenuRepository = SubmenuRepository()
    submenu: SubmenuIn = await submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    dish_repo: DishesRepository = DishesRepository()
    dish: DishIn = await dish_repo.create(DishIn(**dish_data), submenu.id)

    async def fin() -> None:
        await menu_repo.delete(menu.id)
        await submenu_repo.delete(submenu.id)
        await dish_repo.delete(dish.id)
        await RedisTools().redis_client.flushdb()

    yield [menu.id, dish]
    await fin()


@pytest.fixture
async def create_dp(request, menu_data: dict, submenu_data: dict, dish_data: dict):
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = await menu_repo.create(MenuIn(**menu_data))

    submenu_repo: SubmenuRepository = SubmenuRepository()
    submenu: SubmenuIn = await submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    dish_repo: DishesRepository = DishesRepository()
    dish: DishIn = await dish_repo.create(DishIn(**dish_data), submenu.id)

    async def fin() -> None:
        await menu_repo.delete(menu.id)
        await submenu_repo.delete(submenu.id)
        await dish_repo.delete(dish.id)
        await RedisTools().redis_client.flushdb()

    yield [menu, submenu, dish]
    await fin()


@pytest.fixture(autouse=True)
def menu_data() -> dict:
    return {'title': 'My menu', 'description': 'My description'}


@pytest.fixture(autouse=True)
def submenu_data() -> dict:
    return {'title': 'My submenu', 'description': 'My description'}
