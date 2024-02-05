from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import metadata, get_db
from src.config import DB_HOST_TEST, DB_PASS_TEST, DB_NAME_TEST, DB_PORT_TEST, DB_USER_TEST
from main import app
import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenusRepository
from src.schemas.dishes import DishIn
from src.schemas.menus import MenuIn
from src.schemas.submenus import SubmenuIn
from starlette.routing import NoMatchFound

# Конфигурация базы данных для тестов
DATABASE_URL_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine_test = create_engine(DATABASE_URL_TEST)
metadata.bind = engine_test
sessionmaker_test = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)



def reverse_operation(client: TestClient, operation_name: str, **path_params) -> str:
    try:
        path = client.app.url_path_for(operation_name, **path_params)
        return client.base_url + path
    except NoMatchFound:
        raise NoMatchFound(f"Route for operation '{operation_name}' not found.")


# Контекст для изменения зависимости get_db() в тестах
@contextmanager
def override_get_db() -> Generator:
    db = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()

# Фикстура для создания сессии базы данных в тестах
@pytest.fixture(scope="session")
def db() -> Generator:
    try:
        db = sessionmaker_test()
        yield db
    finally:
        db.close()

# Фикстура для настройки базы данных перед запуском тестов
@pytest.fixture(scope='session', autouse=True)
def setup_db() -> None:
    with override_get_db() as db:
        assert db.bind.url.database == DB_NAME_TEST
        metadata.drop_all(engine_test)
        metadata.create_all(engine_test)
        db.commit()

# Фикстура клиента для тестов
@pytest.fixture(scope="module")
def client(db: sessionmaker) -> Generator:
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app, backend_options={"use_uvloop": True})
    with client as c:
        yield c

# Фикстура для создания меню
@pytest.fixture
def create_menu(request, menu_data: dict) -> MenuIn:
    menu_repo = MenusRepository()
    menu = menu_repo.create(MenuIn(**menu_data))

    def fin() -> None:
        menu_repo.delete(menu.id)

    request.addfinalizer(fin)
    return menu

# Фикстура для создания подменю
@pytest.fixture
def create_submenu(request, menu_data: dict, submenu_data: dict) -> SubmenuIn:
    menu_repo = MenusRepository()
    menu = menu_repo.create(MenuIn(**menu_data))
    submenu_repo = SubmenusRepository()
    submenu = submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    def fin() -> None:
        menu_repo.delete(menu.id)
        submenu_repo.delete(submenu.id)

    request.addfinalizer(fin)
    return submenu

# Фикстура для создания блюда
@pytest.fixture
def create_dish(request, menu_data: dict, submenu_data: dict, dish_data: dict) -> list:
    menu_repo = MenusRepository()
    menu = menu_repo.create(MenuIn(**menu_data))

    submenu_repo = SubmenusRepository()
    submenu = submenu_repo.create(SubmenuIn(**submenu_data), menu.id)

    dish_repo = DishesRepository()
    dish = dish_repo.create(DishIn(**dish_data), submenu.id)

    def fin() -> None:
        menu_repo.delete(menu.id)
        submenu_repo.delete(submenu.id)
        dish_repo.delete(dish.id)

    request.addfinalizer(fin)
    return [menu.id, dish]

@pytest.fixture(autouse=True)
def menu_data():
    return {'title': 'My menu', 'description': 'My description'}


@pytest.fixture(autouse=True)
def submenu_data():
    return {'title': 'My submenu', 'description': 'My description'}