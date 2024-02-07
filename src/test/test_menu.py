from http import HTTPStatus

from fastapi.testclient import TestClient

from src.db.database import get_db
from src.models.models import Menu
from src.repositories.menus import MenusRepository
from src.test.revers import reverse_operation


class TestMenu:
    def test_read_menus(self, client: TestClient) -> None:
        response = client.get(reverse_operation('read_menus'))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []
        assert MenusRepository().read_all() == []

    def test_create_menu(self, client: TestClient, menu_data: dict) -> None:
        response_create = client.post(reverse_operation('create_menu'), json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED

        menu_id = str(response_create.json()['id'])
        menu = MenusRepository().read(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        MenusRepository().delete(menu_id)

    def test_read_menu(self, client: TestClient, create_menu: Menu) -> None:
        response_read = client.get(reverse_operation('read_menu', menu_id=create_menu.id))
        assert response_read.status_code == HTTPStatus.OK
        assert response_read.json()['title'] == create_menu.title
        assert response_read.json()['description'] == create_menu.description

    def test_update_menu(self, client: TestClient, create_menu: Menu) -> None:
        updated_data: dict = {'title': 'Updated menu', 'description': 'Updated description'}
        response_update = client.patch(
            reverse_operation('update_menu', menu_id=create_menu.id),
            json=updated_data
        )
        assert response_update.status_code == HTTPStatus.OK

        updated_menu = MenusRepository().read(create_menu.id)
        assert updated_menu is not None
        assert updated_menu.title == updated_data['title']
        assert updated_menu.description == updated_data['description']

    def test_delete_menu(self, client: TestClient, create_menu: Menu) -> None:
        response_delete = client.delete(reverse_operation('delete_menu', menu_id=create_menu.id))
        assert response_delete.status_code == HTTPStatus.OK

        with get_db() as session:
            deleted_menu = session.query(Menu).filter(Menu.id == create_menu.id).first()
            assert deleted_menu is None
