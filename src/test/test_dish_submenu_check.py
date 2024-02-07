from decimal import Decimal
from http import HTTPStatus

import pytest

from src.db.database import get_db
from src.models.models import Menu
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.test.revers import reverse_operation


@pytest.fixture(autouse=True)
def dish_data() -> list[dict]:
    dishes: list[dict] = [
        {'title': 'My dish', 'description': 'My description', 'price': '1111.01'},
        {'title': 'My dish 2', 'description': 'My description 2', 'price': '1111.01'},
    ]
    return dishes


class TestDishSubmenu:
    menu_id = None
    submenu_id = None
    dish_id = None
    dish_id_two = None

    def test_create_menu(self, client, menu_data: dict) -> None:
        response = client.post(reverse_operation('create_menu'), json=menu_data)
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.menu_id = str(response.json()['id'])

        menu = MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_create_submenu(self, client, submenu_data: dict) -> None:
        response = client.post(
            reverse_operation('create_submenu', menu_id=self.__class__.menu_id),
            json=submenu_data
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.submenu_id = str(response.json()['id'])

        submenu = SubmenuRepository().read(self.__class__.submenu_id)
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_create_dish_one(self, client, dish_data: list[dict]) -> None:
        response = client.post(
            reverse_operation(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            ),
            json=dish_data[0],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id = (response.json()['id'])

        dish = DishesRepository().read(self.__class__.dish_id)
        assert dish is not None
        assert dish.title == dish_data[0]['title']
        assert dish.description == dish_data[0]['description']
        assert dish.price == Decimal(dish_data[0]['price'])

    def test_create_dish_two(self, client, dish_data: list[dict]) -> None:
        response = client.post(
            reverse_operation(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            ),
            json=dish_data[1],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id_two = (response.json()['id'])

        dish = DishesRepository().read(self.__class__.dish_id_two)
        assert dish is not None
        assert dish.title == dish_data[1]['title']
        assert dish.description == dish_data[1]['description']
        assert dish.price == Decimal(dish_data[1]['price'])

    def test_read_menu_one(self, client, menu_data: dict) -> None:
        response = client.get(reverse_operation('read_menu', menu_id=self.__class__.menu_id))
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = MenusRepository().read(str(self.__class__.menu_id))
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_read_submenu(self, client, submenu_data: dict) -> None:
        response = client.get(
            reverse_operation(
                'read_submenu',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['title'] == submenu_data['title']
        assert response.json()['description'] == submenu_data['description']

        submenu = SubmenuRepository().read(str(self.__class__.submenu_id))
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_delete_submenu(self, client) -> None:
        response = client.delete(
            reverse_operation(
                'delete_submenu',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK

        submenu = SubmenuRepository().read(str(self.__class__.submenu_id))
        assert submenu is None

    def test_read_submenus(self, client) -> None:
        response = client.get(reverse_operation('read_submenus', menu_id=self.__class__.menu_id))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        submenus = SubmenuRepository().read_all()
        assert submenus == []

    def test_read_dishes(self, client) -> None:
        response = client.get(
            reverse_operation(
                'read_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        dishes = DishesRepository().read_all()
        assert dishes == []

    def test_read_menu_two(self, client, menu_data: dict) -> None:
        response = client.get(reverse_operation('read_menu', menu_id=self.__class__.menu_id))
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = MenusRepository().read(str(self.__class__.menu_id))
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    def test_delete_menu(self, client) -> None:
        response = client.delete(reverse_operation('delete_menu', menu_id=self.__class__.menu_id))
        assert response.status_code == HTTPStatus.OK

        with get_db() as session:
            deleted_menu = session.query(Menu).filter(Menu.id == self.__class__.menu_id).first()
            assert deleted_menu is None

    def test_read_menus(self, client) -> None:
        response = client.get(reverse_operation('read_menus'))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        assert MenusRepository().read_all() == []
