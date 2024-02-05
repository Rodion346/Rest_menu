from decimal import Decimal
from http import HTTPStatus
import pytest
from src.db.database import get_db
from src.models.models import Menu
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenusRepository
from src.repositories.dishes import DishesRepository


@pytest.fixture(autouse=True)
def dish_data():
    dishes = [
        {'title': 'My dish', 'description': 'My description', 'price': '1111.01'},
        {'title': 'My dish 2', 'description': 'My description 2', 'price': '1111.01'},
    ]
    return dishes


class TestDishSubmenu:
    menu_id = None
    submenu_id = None
    dish_id = None
    dish_id_two = None
    def test_create_menu(self, client, menu_data):
        response = client.post('/api/v1/menus', json=menu_data)
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.menu_id = str(response.json()['id'])

        menu = MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_create_submenu(self, client, submenu_data):
        response = client.post(
            f'/api/v1/menus/{self.__class__.menu_id}/submenus', json=submenu_data
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.submenu_id = str(response.json()['id'])

        submenu = SubmenusRepository().read(self.__class__.submenu_id)
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_create_dish_one(self, client, dish_data):
        response = client.post(
            f'/api/v1/menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}/dishes',
            json=dish_data[0],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id = str(response.json()['id'])

        dish = DishesRepository().read(self.__class__.dish_id)
        assert dish is not None
        assert dish.title == dish_data[0]['title']
        assert dish.description == dish_data[0]['description']
        assert dish.price == Decimal(dish_data[0]['price'])

    def test_create_dish_two(self, client, dish_data):
        response = client.post(
            f'/api/v1/menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}/dishes',
            json=dish_data[1],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id_two = str(response.json()['id'])

        dish = DishesRepository().read(self.__class__.dish_id_two)
        assert dish is not None
        assert dish.title == dish_data[1]['title']
        assert dish.description == dish_data[1]['description']
        assert dish.price == Decimal(dish_data[1]['price'])

    def test_read_menu_one(self, client, menu_data):
        response = client.get(f'/api/v1/menus/{self.__class__.menu_id}')
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_read_submenu(self, client, submenu_data):
        response = client.get(f'/api/v1/menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}')
        assert response.status_code == HTTPStatus.OK
        assert response.json()['title'] == submenu_data['title']
        assert response.json()['description'] == submenu_data['description']

        submenu = SubmenusRepository().read(self.__class__.submenu_id)
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_delete_submenu(self, client):
        response = client.delete(f'/api/v1/menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}')
        assert response.status_code == HTTPStatus.OK

        submenu = SubmenusRepository().read(self.__class__.submenu_id)
        assert submenu is None

    def test_read_submenus(self, client):
        response = client.get(f'/api/v1/menus/{self.__class__.menu_id}/submenus')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        submenus = SubmenusRepository().read_all()
        assert submenus == []

    def test_read_dishes(self, client):
        response = client.get(
            f'/api/v1/menus/{self.__class__.menu_id}/submenus/{self.__class__.submenu_id}/dishes'
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        dishes = DishesRepository().read_all()

        assert dishes == []

    def test_read_menu_two(self, client, menu_data):
        response = client.get(f'/api/v1/menus/{self.__class__.menu_id}')
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_delete_menu(self, client):
        response = client.delete(f'/api/v1/menus/{self.__class__.menu_id}')
        assert response.status_code == HTTPStatus.OK

        with get_db() as session:
            deleted_menu = session.query(Menu).filter(Menu.id == self.__class__.menu_id).first()
            assert deleted_menu is None

    def test_read_menus(self, client):
        response = client.get('/api/v1/menus')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        assert MenusRepository().read_all() == []