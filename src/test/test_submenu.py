from http import HTTPStatus

from starlette.testclient import TestClient

from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenusRepository
from src.models.models import Menu, Submenu
from src.test.conftest import reverse_operation


class TestSubMenu:

    def test_create_menu(self, client: TestClient, menu_data: dict) -> None:
        response_create_menu = client.post(reverse_operation(client, "create_menu"), json=menu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED

        menu_id = str(response_create_menu.json()['id'])
        menu = MenusRepository().read(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        MenusRepository().delete(menu.id)

    def test_read_submenus(self, client: TestClient, create_menu: Menu) -> None:
        response_read_submenus = client.get(reverse_operation(client, "read_submenus", menu_id=create_menu.id))
        assert response_read_submenus.status_code == HTTPStatus.OK
        assert response_read_submenus.json() == []

    def test_create_submenu(self, client: TestClient, submenu_data: dict, create_menu: Menu) -> None:
        response_create_submenu = client.post(
            reverse_operation(client, "create_submenu", menu_id=create_menu.id), json=submenu_data
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED

        submenu_id = str(response_create_submenu.json()['id'])
        submenu = SubmenusRepository().read(submenu_id)

        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_update_submenu(self, client: TestClient, create_submenu: Submenu) -> None:
        updated_data = {'title': 'Updated submenu', 'description': 'Updated description'}
        response_update_submenu = client.patch(
            reverse_operation(client, "update_submenu", menu_id=create_submenu.menu_id,submenu_id=create_submenu.id), json=updated_data
        )
        assert response_update_submenu.status_code == HTTPStatus.OK

        submenu = SubmenusRepository().read(create_submenu.id)
        assert submenu is not None
        assert submenu.title == updated_data['title']
        assert submenu.description == updated_data['description']

    def test_delete_submenu(self, client: TestClient, create_submenu: Submenu) -> None:
        response_delete_submenu = client.delete(
            reverse_operation(client, "delete_submenu", menu_id=create_submenu.menu_id,submenu_id=create_submenu.id)
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        submenu = SubmenusRepository().read(create_submenu.id)
        assert submenu is None