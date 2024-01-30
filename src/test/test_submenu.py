from http import HTTPStatus
import pytest
from sqlalchemy.orm import Session
from src.models import Menu, Submenu

@pytest.fixture
def menu_data():
    return {'title': 'My menu', 'description': 'My description'}

@pytest.fixture
def submenu_data():
    return {'title': 'My submenu', 'description': 'My description'}

class TestSubMenu:

    def test_create_menu(self, client, db: Session, menu_data):
        response_create_menu = client.post('/api/v1/menus', json=menu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED

        submenu_menu_id = str(response_create_menu.json()['id'])
        menu = db.query(Menu).get(submenu_menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        response_delete_menu = client.delete(f'/api/v1/menus/{submenu_menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).get(submenu_menu_id)
        assert menu_after_delete is None

    def test_read_submenus(self, client, db: Session, submenu_data):
        response_create_menu = client.post('/api/v1/menus', json=submenu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        submenu_menu_id = str(response_create_menu.json()['id'])

        response_read_submenus = client.get(f'/api/v1/menus/{submenu_menu_id}/submenus')
        assert response_read_submenus.status_code == HTTPStatus.OK
        assert response_read_submenus.json() == []

        response_delete_menu = client.delete(f'/api/v1/menus/{submenu_menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).get(submenu_menu_id)
        assert menu_after_delete is None

    def test_create_submenu(self, client, db: Session, submenu_data):
        response_create_menu = client.post('/api/v1/menus', json=submenu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        submenu_menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{submenu_menu_id}/submenus', json=submenu_data
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED

        submenu_id = str(response_create_submenu.json()['id'])
        submenu = db.query(Submenu).get(submenu_id)

        assert submenu is not None
        assert submenu.title == submenu_data['title']
        assert submenu.description == submenu_data['description']

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        response_delete_menu = client.delete(f'/api/v1/menus/{submenu_menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        submenu_after_delete = db.query(Submenu).get(submenu_id)
        assert submenu_after_delete is None

    def test_update_submenu(self, client, db: Session, submenu_data):
        response_create_menu = client.post('/api/v1/menus', json=submenu_data)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        submenu_menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{submenu_menu_id}/submenus', json=submenu_data
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        updated_data = {'title': 'Updated submenu', 'description': 'Updated description'}
        response_update_submenu = client.patch(
            f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}', json=updated_data
        )
        assert response_update_submenu.status_code == HTTPStatus.OK
        assert response_update_submenu.json()['title'] == updated_data['title']
        assert response_update_submenu.json()['description'] == updated_data['description']

        submenu = db.query(Submenu).get(submenu_id)
        assert submenu is not None
        assert submenu.title == updated_data['title']
        assert submenu.description == updated_data['description']

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        response_delete_menu = client.delete(f'/api/v1/menus/{submenu_menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        submenu_after_delete = db.query(Submenu).get(submenu_id)
        assert submenu_after_delete is None

    def test_delete_submenu(self, client, db: Session):
        response_create_menu = client.post('/api/v1/menus',
                                           json={'title': 'Test Menu', 'description': 'Test Description'})
        assert response_create_menu.status_code == HTTPStatus.CREATED
        submenu_menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{submenu_menu_id}/submenus',
            json={'title': 'Test Submenu', 'description': 'Test Description'}
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{submenu_menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        submenu = db.query(Submenu).get(submenu_id)
        assert submenu is None

        response_delete_menu = client.delete(f'/api/v1/menus/{submenu_menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu = db.query(Menu).get(submenu_menu_id)
        assert menu is None