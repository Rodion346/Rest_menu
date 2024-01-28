from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import metadata, get_db, Base
from src.config import DB_HOST_TEST, DB_PASS_TEST, DB_NAME_TEST, DB_PORT_TEST, DB_USER_TEST
from main import app
import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager

DATABASE_URL_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_engine(DATABASE_URL_TEST)
metadata.bind = engine_test

sessionmaker_test = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@contextmanager
def override_get_db():
    db = sessionmaker_test()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def db() -> Generator:
    try:
        db = sessionmaker_test()
        yield db
    finally:
        db.close()

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    with override_get_db() as db:
        assert db.bind.url.database == DB_NAME_TEST
        metadata.drop_all(engine_test)
        metadata.create_all(engine_test)
        db.commit()



@pytest.fixture(scope="module")
def client(db) -> Generator:
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app, backend_options={"use_uvloop": True})
    with client as c:
        yield c


@pytest.fixture(autouse=True)
def fixture_menu():
    menus = [
        {'title': 'My menu', 'description': 'My description'},
        {'title': 'Updated menu', 'description': 'Updated description'},
    ]
    return menus


@pytest.fixture(autouse=True)
def fixture_submenu():
    submenus = [
        {'title': 'My submenu', 'description': 'My description'},
        {'title': 'Updated submenu', 'description': 'Updated description'},
    ]
    return submenus


@pytest.fixture(autouse=True)
def fixture_dish():
    dishes = [
        {'title': 'My dish', 'description': 'My description', 'price': 1111.01},
        {'title': 'My dish 2', 'description': 'My description 2', 'price': 1111.01},
        {'title': 'Updated dish','description': 'Updated description','price': 2222.01,},
    ]
    return dishes


@pytest.fixture(scope='session', autouse=True)
def cleanup_db(request):
    yield
    with override_get_db() as db:
        metadata.drop_all(engine_test)
        db.commit()