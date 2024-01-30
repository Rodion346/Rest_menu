import pytest
from http import HTTPStatus
from src.models import Menu
from sqlalchemy.orm import Session

@pytest.fixture
def menu_data():
    return {'title': 'My menu', 'description': 'My description'}

class TestMenu:

    def test_read_menus(self, client, db: Session):
        response = client.get('/api/v1/menus')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

        menus_in_db = db.query(Menu).all()
        assert len(menus_in_db) == 0

    def test_create_menu(self, client, db: Session, menu_data):
        response_create = client.post('/api/v1/menus', json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED

        menu_id = str(response_create.json()['id'])
        menu = db.query(Menu).get(menu_id)

        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        response_delete = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).get(menu_id)
        assert menu_after_delete is None

    def test_read_menu(self, client, db: Session, menu_data):
        response_create = client.post('/api/v1/menus', json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED
        menu_id = str(response_create.json()['id'])

        response_read = client.get(f'/api/v1/menus/{menu_id}')
        assert response_read.status_code == HTTPStatus.OK
        assert response_read.json()['title'] == menu_data['title']
        assert response_read.json()['description'] == menu_data['description']

        menu = db.query(Menu).get(menu_id)
        assert menu is not None
        assert menu.title == menu_data['title']
        assert menu.description == menu_data['description']

        response_delete = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).get(menu_id)
        assert menu_after_delete is None

    def test_update_menu(self, client, db: Session, menu_data):
        response_create = client.post('/api/v1/menus', json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED
        menu_id = str(response_create.json()['id'])

        updated_data = {'title': 'Updated menu', 'description': 'Updated description'}
        response_update = client.patch(f'/api/v1/menus/{menu_id}', json=updated_data)
        assert response_update.status_code == HTTPStatus.OK
        assert response_update.json()['title'] == updated_data['title']
        assert response_update.json()['description'] == updated_data['description']

        menu = db.query(Menu).get(menu_id)
        assert menu is not None
        assert menu.title == updated_data['title']
        assert menu.description == updated_data['description']

        response_delete = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).get(menu_id)
        assert menu_after_delete is None

    def test_delete_menu(self, client, db: Session, menu_data):
        response_create = client.post('/api/v1/menus', json=menu_data)
        assert response_create.status_code == HTTPStatus.CREATED
        menu_id = str(response_create.json()['id'])

        response_delete = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete.status_code == HTTPStatus.OK

        menu = db.query(Menu).get(menu_id)
        assert menu is None