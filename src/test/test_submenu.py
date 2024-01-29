from http import HTTPStatus
import pytest
from sqlalchemy.orm import Session
from src.models import Menu, Submenu

class TestSubMenu:
    menu_id = None
    submenu_id = None

    def test_create_menu(self, client, fixture_menu, db: Session):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])

        menu = db.query(Menu).filter(Menu.id == pytest.menu_id).first()
        assert menu is not None
        assert menu.title == fixture_menu[0]['title']
        assert menu.description == fixture_menu[0]['description']

    def test_read_submenus(self, client):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}/submenus')
        assert response.status_code == 200
        assert response.json() == []

    def test_create_submenu(self, client, fixture_submenu, db: Session):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus', json=fixture_submenu[0]
        )
        assert response.status_code == HTTPStatus.CREATED
        pytest.submenu_id = str(response.json()['id'])

        submenu = db.query(Submenu).filter(Submenu.id == pytest.submenu_id).first()
        assert submenu is not None
        assert submenu.title == fixture_submenu[0]['title']
        assert submenu.description == fixture_submenu[0]['description']

    def test_update_submenu(self, client, fixture_submenu, db: Session):
        response = client.patch(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}',
            json=fixture_submenu[1],
        )
        assert response.json()['title'] == fixture_submenu[1]['title']
        assert response.json()['description'] == fixture_submenu[1]['description']

        submenu = db.query(Submenu).filter(Submenu.id == pytest.submenu_id).first()
        assert submenu is not None
        assert submenu.title == fixture_submenu[1]['title']
        assert submenu.description == fixture_submenu[1]['description']

    def test_delete_submenu(self, client, db: Session):
        response = client.delete(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}'
        )
        assert response.status_code == HTTPStatus.OK

        submenu = db.query(Submenu).filter(Submenu.id == pytest.submenu_id).first()
        assert submenu is None

        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK

        menu = db.query(Menu).filter(Menu.id == pytest.menu_id).first()
        assert menu is None