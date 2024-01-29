from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session
from src.models import Menu, Submenu, Dishes

class TestDishSubmenu:
    menu_id = None
    submenu_id = None
    dish_id = None

    def test_create_menu(self, client, fixture_menu):
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        pytest.menu_id = str(response.json()['id'])

    def test_create_submenu(self, client, fixture_submenu):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus', json=fixture_submenu[0]
        )
        assert response.status_code == 201
        pytest.submenu_id = str(response.json()['id'])

    def test_create_dish_one(self, client, fixture_dish, db: Session):
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

    def test_create_dish_two(self, client, fixture_dish, db: Session):
        response = client.post(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes',
            json=fixture_dish[1],
        )
        assert response.status_code == 201
        pytest.dish_id = str(response.json()['id'])

        dish = db.query(Dishes).filter(Dishes.id == pytest.dish_id).first()
        assert dish is not None
        assert dish.title == fixture_dish[1]['title']
        assert dish.description == fixture_dish[1]['description']

    def test_read_menu_one(self, client, fixture_menu, db: Session):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}')
        assert response.json()['title'] == fixture_menu[0]['title']
        assert response.json()['description'] == fixture_menu[0]['description']

        menu = db.query(Menu).filter(Menu.id == pytest.menu_id).first()
        assert menu is not None
        assert menu.title == fixture_menu[0]['title']
        assert menu.description == fixture_menu[0]['description']

    def test_read_submenu(self, client, fixture_submenu, db: Session):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == fixture_submenu[0]['title']
        assert response_json['description'] == fixture_submenu[0]['description']

        submenu = db.query(Submenu).filter(Submenu.id == pytest.submenu_id).first()
        assert submenu is not None
        assert submenu.title == fixture_submenu[0]['title']
        assert submenu.description == fixture_submenu[0]['description']

    def test_delete_submenu(self, client):
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}')
        assert response.status_code == HTTPStatus.OK

    def test_read_submenus(self, client, db: Session):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}/submenus')
        assert response.status_code == 200
        assert response.json() == []

        submenus = db.query(Submenu).filter(Submenu.menu_id == pytest.menu_id).all()
        assert len(submenus) == 0

    def test_read_dishes(self, client, db: Session):
        response = client.get(
            f'/api/v1/menus/{pytest.menu_id}/submenus/{pytest.submenu_id}/dishes'
        )
        assert response.status_code == 200
        assert response.json() == []

        dishes = db.query(Dishes).filter(Dishes.submenu_id == pytest.submenu_id).all()
        assert len(dishes) == 0

    def test_read_menu_two(self, client, fixture_menu, db: Session):
        response = client.get(f'/api/v1/menus/{pytest.menu_id}')
        print(response.json)
        assert response.json()['title'] == fixture_menu[0]['title']
        assert response.json()['description'] == fixture_menu[0]['description']

        menu = db.query(Menu).filter(Menu.id == pytest.menu_id).first()
        assert menu is not None
        assert menu.title == fixture_menu[0]['title']
        assert menu.description == fixture_menu[0]['description']

    def test_delete_menu(self, client):
        response = client.delete(f'/api/v1/menus/{pytest.menu_id}')
        assert response.status_code == HTTPStatus.OK

    def test_read_menus(self, client, db: Session):
        response = client.get('/api/v1/menus')
        assert response.status_code == 200
        assert response.json() == []

        menus = db.query(Menu).all()
        assert len(menus) == 0