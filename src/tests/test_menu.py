from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.models.models import Menu
from src.repositories.menus import MenusRepository
from src.tests.revers import reverse_operation


@pytest.fixture
def dish_data() -> dict[str, str]:
    return {'title': 'My dish', 'description': 'My description', 'price': '1111.01'}


class TestMenu:
    async def test_read_menus(self, ac: AsyncClient):
        response = await ac.get(reverse_operation('read_menus'))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []
        assert await MenusRepository().read_all() == []

    async def test_create_menu(self, ac: AsyncClient, menu_data: dict) -> None:
        response_create = await ac.post(reverse_operation('create_menu'), json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED

        menu_id = response_create.json()['id']
        menu = await MenusRepository().read(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        await MenusRepository().delete(menu_id)

    async def test_read_menu(self, ac: AsyncClient, create_menu: Menu) -> None:
        response_read = await ac.get(reverse_operation('read_menu', menu_id=create_menu.id))
        assert response_read.status_code == HTTPStatus.OK
        assert response_read.json()['title'] == create_menu.title
        assert response_read.json()['description'] == create_menu.description

    async def test_update_menu(self, ac: AsyncClient, create_menu: Menu) -> None:
        updated_data: dict = {'title': 'Updated menu', 'description': 'Updated description'}
        response_update = await ac.patch(
            reverse_operation('update_menu', menu_id=create_menu.id),
            json=updated_data
        )
        assert response_update.status_code == HTTPStatus.OK

        updated_menu = await MenusRepository().read(create_menu.id)
        assert updated_menu is not None
        assert updated_menu.title == updated_data['title']
        assert updated_menu.description == updated_data['description']

    async def test_delete_menu(self, ac: AsyncClient, create_menu: Menu) -> None:
        response_delete = await ac.delete(reverse_operation('delete_menu', menu_id=create_menu.id))
        assert response_delete.status_code == HTTPStatus.OK
        deleted_menu = await MenusRepository().read(create_menu.id)
        assert deleted_menu is None

    async def test_DP(self, ac: AsyncClient, create_dp, menu_data, submenu_data, dish_data) -> None:
        response_dp = await ac.get(reverse_operation('all_dep'))

        assert response_dp.status_code == 200
        data = response_dp.json()
        assert isinstance(data, list)
        assert len(data) == 1  # Assuming one created menu
        menu = data[0]
        assert 'id' in menu
        assert 'title' in menu
        assert 'description' in menu
        assert 'submenus' in menu
        assert isinstance(menu['submenus'], list)
        assert len(menu['submenus']) == 1  # Assuming one created submenu
        submenu = menu['submenus'][0]
        assert 'id' in submenu
        assert 'title' in submenu
        assert 'description' in submenu
        assert 'dishes' in submenu
        assert isinstance(submenu['dishes'], list)
        assert len(submenu['dishes']) == 1  # Assuming one created dish
        dish = submenu['dishes'][0]
        assert 'id' in dish
        assert 'title' in dish
        assert 'description' in dish
        assert 'price' in dish
