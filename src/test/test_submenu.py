from http import HTTPStatus
from src.repositories.menus import MenusRepository
from src.repositories.submenus import SubmenusRepository
from src.models.models import Menu, Submenu


class TestSubMenu:

    def test_create_menu(self, client, menu_data: dict) -> None:
        response_create_menu = client.post('/api/v1/menus', json=menu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED

        menu_id = str(response_create_menu.json()['id'])
        menu = MenusRepository().read(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        MenusRepository().delete(menu.id)

    def test_read_submenus(self, client, create_menu: Menu) -> None:
        response_read_submenus = client.get(f'/api/v1/menus/{create_menu.id}/submenus')
        assert response_read_submenus.status_code == HTTPStatus.OK
        assert response_read_submenus.json() == []

    def test_create_submenu(self, client, submenu_data: dict, create_menu: Menu) -> None:
        response_create_submenu = client.post(
            f'/api/v1/menus/{create_menu.id}/submenus', json=submenu_data
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED

        submenu_id = str(response_create_submenu.json()['id'])
        submenu = SubmenusRepository().read(submenu_id)

        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

    def test_update_submenu(self, client, create_submenu: Submenu) -> None:
        updated_data = {'title': 'Updated submenu', 'description': 'Updated description'}
        response_update_submenu = client.patch(
            f'/api/v1/menus/{create_submenu.menu_id}/submenus/{create_submenu.id}', json=updated_data
        )
        assert response_update_submenu.status_code == HTTPStatus.OK

        submenu = SubmenusRepository().read(create_submenu.id)
        assert submenu is not None
        assert submenu.title == updated_data['title']
        assert submenu.description == updated_data['description']

    def test_delete_submenu(self, client, create_submenu: Submenu) -> None:
        response_delete_submenu = client.delete(
            f'/api/v1/menus/{create_submenu.menu_id}/submenus/{create_submenu.id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        submenu = SubmenusRepository().read(create_submenu.id)
        assert submenu is None