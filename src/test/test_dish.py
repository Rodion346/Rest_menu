from http import HTTPStatus

import pytest


class TestDish:
    menu_id = None
    submenu_id = None
    dish_id = None

    def test_create_submenu(self, client, fixture_menu, fixture_submenu):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus', json=fixture_submenu[0]
        )
        assert response.status_code == 201
        pytest.submenu_id = str(response.json()['id'])

    def test_read_dishes(self, client):
        response = client.get(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.menu_id}/dishes'
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_create_dish(self, client, fixture_dish):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes',
            json=fixture_dish[0],
        )
        assert response.status_code == 201
        pytest.dish_id = str(response.json()['id'])

    def test_update_dish(self, client, fixture_dish):
        response = client.patch(
            f'/api/v1/menus/'
            f'{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes/{pytest.dish_id}',
            json=fixture_dish[1],
        )
        assert response.json()['title'] == fixture_dish[1]['title']
        assert response.json()['description'] == fixture_dish[1]['description']
        assert response.json()['price'] == str(fixture_dish[1]['price'])

    def test_delete_dish(self, client):
        response = client.delete(
            f'/api/v1/menus/'
            f'{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes/{pytest.dish_id}'
        )
        assert response.status_code == HTTPStatus.OK
        response = client.delete(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}'
        )
        assert response.status_code == HTTPStatus.OK
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK