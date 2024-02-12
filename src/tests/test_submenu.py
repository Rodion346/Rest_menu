from http import HTTPStatus

from httpx import AsyncClient

from src.models.models import Menu, Submenu
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenuRepository
from src.tests.revers import reverse_operation


class TestSubMenu:

    async def test_create_menu(self, ac: AsyncClient, menu_data: dict) -> None:
        response_create_menu = await ac.post(reverse_operation('create_menu'), json=menu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED

        menu_id = response_create_menu.json()['id']
        menu = await MenusRepository().read(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        await MenusRepository().delete(menu.id)

    async def test_read_submenus(self, ac: AsyncClient, create_menu: Menu) -> None:
        response_read_submenus = await ac.get(reverse_operation('read_submenus', menu_id=create_menu.id))
        assert response_read_submenus.status_code == HTTPStatus.OK
        assert response_read_submenus.json() == []

    async def test_create_submenu(self, ac: AsyncClient, submenu_data: dict, create_menu: Menu) -> None:
        response_create_submenu = await ac.post(
            reverse_operation('create_submenu', menu_id=create_menu.id), json=submenu_data
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED

        submenu_id = response_create_submenu.json()['id']
        submenu = await SubmenuRepository().read(submenu_id)

        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    async def test_update_submenu(self, ac: AsyncClient, create_submenu: Submenu) -> None:
        updated_data: dict = {'title': 'Updated submenu', 'description': 'Updated description'}
        response_update_submenu = await ac.patch(
            reverse_operation('update_submenu', menu_id=create_submenu.menu_id, submenu_id=create_submenu.id), json=updated_data
        )
        assert response_update_submenu.status_code == HTTPStatus.OK

        submenu = await SubmenuRepository().read(create_submenu.id)
        assert submenu is not None
        assert submenu.title == updated_data['title']
        assert submenu.description == updated_data['description']

    async def test_delete_submenu(self, ac: AsyncClient, create_submenu: Submenu) -> None:
        response_delete_submenu = await ac.delete(
            reverse_operation('delete_submenu', menu_id=create_submenu.menu_id, submenu_id=create_submenu.id)
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        submenu = await SubmenuRepository().read(create_submenu.id)
        assert submenu is None
