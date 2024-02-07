from contextlib import contextmanager
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
)
from src.db.database import get_db, metadata
from src.redis.redis_manage import RedisTools
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.schemas.dishes import DishIn
from src.schemas.menus import MenuIn
from src.schemas.submenus import SubmenuIn

DATABASE_URL_TEST: str = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"  # noqa: E231
engine_test = create_engine(DATABASE_URL_TEST)
metadata.bind = engine_test
sessionmaker_test: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@contextmanager
def override_get_db() -> Generator:
    db: sessionmaker = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session')
def db() -> Generator:
    try:
        db: sessionmaker = sessionmaker_test()
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session', autouse=True)
def setup_db() -> None:
    with override_get_db() as db:
        assert db.bind.url.database == DB_NAME_TEST
        metadata.drop_all(engine_test)
        metadata.create_all(engine_test)
        db.commit()


@pytest.fixture(scope='module')
def client(db: sessionmaker) -> Generator:
    app.dependency_overrides[get_db] = lambda: db
    client: TestClient = TestClient(app, backend_options={'use_uvloop': True})
    with client as c:
        yield c


@pytest.fixture
def create_menu(request, menu_data: dict) -> MenuIn:
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = menu_repo.create(MenuIn(**menu_data))

    def fin() -> None:
        menu_repo.delete(menu.id)
        RedisTools().redis_client.flushdb()

    request.addfinalizer(fin)
    return menu


@pytest.fixture
def create_submenu(request, menu_data: dict, submenu_data: dict) -> SubmenuIn:
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = menu_repo.create(MenuIn(**menu_data))
    submenu_repo: SubmenuRepository = SubmenuRepository()
    submenu: SubmenuIn = submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    def fin() -> None:
        menu_repo.delete(menu.id)
        submenu_repo.delete(submenu.id)
        RedisTools().redis_client.flushdb()

    request.addfinalizer(fin)
    return submenu


@pytest.fixture
def create_dish(request, menu_data: dict, submenu_data: dict, dish_data: dict) -> list:
    menu_repo: MenusRepository = MenusRepository()
    menu: MenuIn = menu_repo.create(MenuIn(**menu_data))

    submenu_repo: SubmenuRepository = SubmenuRepository()
    submenu: SubmenuIn = submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    dish_repo: DishesRepository = DishesRepository()
    dish: DishIn = dish_repo.create(DishIn(**dish_data), submenu.id)

    def fin() -> None:
        menu_repo.delete(menu.id)
        submenu_repo.delete(submenu.id)
        dish_repo.delete(dish.id)
        RedisTools().redis_client.flushdb()

    request.addfinalizer(fin)
    return [menu.id, dish]


@pytest.fixture(autouse=True)
def menu_data() -> dict:
    return {'title': 'My menu', 'description': 'My description'}


@pytest.fixture(autouse=True)
def submenu_data() -> dict:
    return {'title': 'My submenu', 'description': 'My description'}
