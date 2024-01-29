from http import HTTPStatus
from src.models import Menu
from sqlalchemy.orm import Session
import pytest

@pytest.fixture(autouse=True)
def fixture_menu():
    menus = [
        {'title': 'My menu', 'description': 'My description'},
        {'title': 'Updated menu', 'description': 'Updated description'},
    ]
    return menus



class TestMenu:
    menu_id = None

    def test_read_menus(self, client, db: Session):
        response = client.get('/api/v1/menus')
        assert response.status_code == 200
        assert response.json() == []

    def test_create_menu(self, client, fixture_menu, db: Session):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])

        menu = db.query(Menu).get(pytest.menu_id)
        assert menu is not None
        assert menu.title == fixture_menu[0]['title']
        assert menu.description == fixture_menu[0]['description']

    def test_read_menu(self, client, fixture_menu, db: Session):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}')
        assert response.json()['title'] == fixture_menu[0]['title']
        assert response.json()['description'] == fixture_menu[0]['description']

        menu = db.query(Menu).get(pytest.menu_id)
        assert menu is not None
        assert response.json()['title'] == menu.title
        assert response.json()['description'] == menu.description

    def test_update_menu(self, client, fixture_menu, db: Session):
        response = client.patch(f'/api/v1/menus/{pytest.menu_id}', json=fixture_menu[1])
        assert response.json()['title'] == fixture_menu[1]['title']
        assert response.json()['description'] == fixture_menu[1]['description']

        menu = db.query(Menu).get(pytest.menu_id)
        assert menu is not None
        assert response.json()['title'] == menu.title
        assert response.json()['description'] == menu.description

    def test_delete_menu(self, client, db: Session):
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK

        menu = db.query(Menu).get(pytest.menu_id)
        assert menu is None