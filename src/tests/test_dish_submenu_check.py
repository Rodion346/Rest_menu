from decimal import Decimal
from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy import UUID

from src.admin.exel import disc
from src.repositories.dishes import DishesRepository
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.tests.revers import reverse_operation


@pytest.fixture(autouse=True)
def dish_data() -> list[dict]:
    dishes: list[dict] = [
        {'title': 'My dish', 'description': 'My description', 'price': '1111.01'},
        {'title': 'My dish 2', 'description': 'My description 2', 'price': '1111.01'},
    ]
    return dishes


class TestDishSubmenu:
    menu_id: UUID = None
    submenu_id: UUID = None
    dish_id: UUID = None
    dish_id_two: UUID = None

    async def test_create_menu(self, ac: AsyncClient, menu_data: dict) -> None:
        response = await ac.post(reverse_operation('create_menu'), json=menu_data)
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.menu_id = response.json()['id']

        menu = await MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    async def test_create_submenu(self, ac: AsyncClient, submenu_data: dict) -> None:
        response = await ac.post(
            reverse_operation('create_submenu', menu_id=self.__class__.menu_id),
            json=submenu_data
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.submenu_id = response.json()['id']

        submenu = await SubmenuRepository().read(self.__class__.submenu_id)
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    async def test_create_dish_one(self, ac: AsyncClient, dish_data: list[dict]) -> None:
        response = await ac.post(
            reverse_operation(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            ),
            json=dish_data[0],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id = response.json()['id']

        dish = await DishesRepository().read(self.__class__.dish_id, disc)
        assert dish is not None
        assert dish.title == dish_data[0]['title']
        assert dish.description == dish_data[0]['description']
        assert dish.price == Decimal(dish_data[0]['price'])

    async def test_create_dish_two(self, ac: AsyncClient, dish_data: list[dict]) -> None:
        response = await ac.post(
            reverse_operation(
                'create_dish',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            ),
            json=dish_data[1],
        )
        assert response.status_code == HTTPStatus.CREATED
        self.__class__.dish_id_two = response.json()['id']

        dish = await DishesRepository().read(self.__class__.dish_id_two, disc)
        assert dish is not None
        assert dish.title == dish_data[1]['title']
        assert dish.description == dish_data[1]['description']
        assert dish.price == Decimal(dish_data[1]['price'])

    async def test_read_menu_one(self, ac: AsyncClient, menu_data: dict) -> None:
        response = await ac.get(reverse_operation('read_menu', menu_id=self.__class__.menu_id))
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = await MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    async def test_read_submenu(self, ac: AsyncClient, submenu_data: dict) -> None:
        response = await ac.get(
            reverse_operation(
                'read_submenu',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['title'] == submenu_data['title']
        assert response.json()['description'] == submenu_data['description']

        submenu = await SubmenuRepository().read(self.__class__.submenu_id)
        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    async def test_delete_submenu(self, ac: AsyncClient) -> None:
        response = await ac.delete(
            reverse_operation(
                'delete_submenu',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK

        submenu = await SubmenuRepository().read(self.__class__.submenu_id)
        assert submenu is None

    async def test_read_submenus(self, ac: AsyncClient) -> None:
        response = await ac.get(reverse_operation('read_submenus', menu_id=self.__class__.menu_id))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        submenus = await SubmenuRepository().read_all()
        assert submenus == []

    async def test_read_dishes(self, ac: AsyncClient) -> None:
        response = await ac.get(
            reverse_operation(
                'read_dishes',
                menu_id=self.__class__.menu_id,
                submenu_id=self.__class__.submenu_id
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        dishes = await DishesRepository().read_all()
        assert dishes == []

    async def test_read_menu_two(self, ac: AsyncClient, menu_data: dict) -> None:
        response = await ac.get(reverse_operation('read_menu', menu_id=self.__class__.menu_id))
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        menu = await MenusRepository().read(self.__class__.menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

    async def test_delete_menu(self, ac: AsyncClient) -> None:
        response = await ac.delete(reverse_operation('delete_menu', menu_id=self.__class__.menu_id))
        assert response.status_code == HTTPStatus.OK

        deleted_menu = await MenusRepository().read(self.__class__.menu_id)
        assert deleted_menu is None

    async def test_read_menus(self, ac: AsyncClient) -> None:
        response = await ac.get(reverse_operation('read_menus'))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []
        resp = await MenusRepository().read(self.__class__.menu_id)
        assert resp is None
