from http import HTTPStatus

import pytest


class TestSubMenu:
    menu_id = None
    submenu_id = None

    def test_create_menu(self, client, fixture_menu):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])

    def test_read_submenus(self, client):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}/submenus')
        assert response.status_code == 200
        assert response.json() == []

    def test_create_submenu(self, client, fixture_submenu):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus', json=fixture_submenu[0]
        )
        assert response.status_code == 201
        pytest.submenu_id = str(response.json()['id'])

    def test_update_submenu(self, client, fixture_submenu):
        response = client.patch(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}',
            json=fixture_submenu[1],
        )
        assert response.json()['title'] == fixture_submenu[1]['title']
        assert response.json()['description'] == fixture_submenu[1]['description']

    def test_delete_submenu(self, client):
        response = client.delete(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}'
        )
        assert response.status_code == HTTPStatus.OK
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK