from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from src.models import Menu, Submenu, Dishes

class TestDish:
    menu_id = None
    submenu_id = None
    dish_id = None

    def test_create_submenu(self, client, fixture_menu, fixture_submenu, db: Session):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus', json=fixture_submenu[0]
        )
        assert response.status_code == 201
        pytest.submenu_id = str(response.json()['id'])

        menu = db.query(Menu).filter(Menu.id == pytest.menu_id).first()
        assert menu is not None
        assert menu.title == fixture_menu[0]['title']
        assert menu.description == fixture_menu[0]['description']

        submenu = db.query(Submenu).filter(Submenu.id == pytest.submenu_id).first()
        assert submenu is not None
        assert submenu.title == fixture_submenu[0]['title']
        assert submenu.description == fixture_submenu[0]['description']

    def test_read_dishes(self, client):
        response = client.get(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.menu_id}/dishes'
        )
        assert response.status_code == 200
        assert response.json() == []
    def test_create_dish(self, client, fixture_dish, db: Session):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes',
            json=fixture_dish[0],
        )
        assert response.status_code == 201
        pytest.dish_id = str(response.json()['id'])

        dish = db.query(Dishes).filter(Dishes.id == pytest.dish_id).first()
        assert dish is not None
        assert dish.title == fixture_dish[0]['title']
        assert dish.description == fixture_dish[0]['description']
        assert str(dish.price) == fixture_dish[0]['price']

    def test_update_dish(self, client, fixture_dish, db: Session):
        response = client.patch(
            f'/api/v1/menus/'
            f'{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes/{pytest.dish_id}',
            json=fixture_dish[1],
        )
        assert response.json()['title'] == fixture_dish[1]['title']
        assert response.json()['description'] == fixture_dish[1]['description']
        assert response.json()['price'] == str(fixture_dish[1]['price'])

        dish = db.query(Dishes).filter(Dishes.id == pytest.dish_id).first()
        assert dish is not None
        assert dish.title == fixture_dish[1]['title']
        assert dish.description == fixture_dish[1]['description']
        assert str(dish.price) == fixture_dish[1]['price']

    def test_delete_dish(self, client, db: Session):
        response = client.delete(
            f'/api/v1/menus/'
            f'{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes/{pytest.dish_id}'
        )
        assert response.status_code == HTTPStatus.OK

        dish = db.query(Dishes).filter(Dishes.id == pytest.dish_id).first()
        assert dish is None

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