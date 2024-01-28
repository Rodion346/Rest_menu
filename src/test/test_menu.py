from http import HTTPStatus

import pytest


class TestMenu:
    menu_id = None

    def test_read_menus(self, client):
        response = client.get('/api/v1/menus')
        assert response.status_code == 200
        assert response.json() == []

    def test_create_menu(self, client, fixture_menu):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])

    def test_read_menu(self, client, fixture_menu):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}')
        assert response.json()['title'] == fixture_menu[0]['title']
        assert response.json()['description'] == fixture_menu[0]['description']

    def test_update_menu(self, client, fixture_menu):
        response = client.patch(f'/api/v1/menus/{pytest.menu_id}', json=fixture_menu[1])
        assert response.json()['title'] == fixture_menu[1]['title']
        assert response.json()['description'] == fixture_menu[1]['description']

    def test_delete_menu(self, client):
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK
