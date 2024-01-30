from http import HTTPStatus

import pytest
from sqlalchemy.orm import Session

from src.models import Menu, Submenu, Dishes


@pytest.fixture
def fixture_menu():
    return {'title': 'My menu', 'description': 'My description'}

@pytest.fixture
def fixture_submenu():
    return {'title': 'My submenu', 'description': 'My description'}

@pytest.fixture
def fixture_dish():
    return {'title': 'My dish', 'description': 'My description', 'price': '1111.01'}


class TestDish:

    def test_create_submenu(self, client, fixture_menu, fixture_submenu, db: Session):
        response_create_menu = client.post('/api/v1/menus', json=fixture_menu)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=fixture_submenu
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        assert menu is not None
        assert menu.title == fixture_menu['title']
        assert menu.description == fixture_menu['description']

        submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        assert submenu is not None
        assert submenu.title == fixture_submenu['title']
        assert submenu.description == fixture_submenu['description']

        response_delete_menu = client.delete(
            f'/api/v1/menus/{menu_id}'
        )
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).filter(Menu.id == menu_id).first()
        assert menu_after_delete is None

        submenu_after_delete = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        assert submenu_after_delete is None

    def test_read_dishes(self, client, fixture_menu, fixture_submenu, fixture_dish, db: Session):
        response_create_menu = client.post('/api/v1/menus', json=fixture_menu)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=fixture_submenu
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        response_read_dishes = client.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
        )
        assert response_read_dishes.status_code == HTTPStatus.OK
        assert response_read_dishes.json() == []

        response_delete_menu = client.delete(
            f'/api/v1/menus/{menu_id}'
        )
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).filter(Menu.id == menu_id).first()
        assert menu_after_delete is None

        submenu_after_delete = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        assert submenu_after_delete is None

    def test_create_dish(self, client, fixture_menu, fixture_submenu, fixture_dish, db: Session):
        response_create_menu = client.post('/api/v1/menus', json=fixture_menu)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=fixture_submenu
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        response_create_dish = client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
            json=fixture_dish
        )
        assert response_create_dish.status_code == HTTPStatus.CREATED

        dish_id = str(response_create_dish.json()['id'])
        dish = db.query(Dishes).filter(Dishes.id == dish_id).first()

        assert dish is not None
        assert dish.title == fixture_dish['title']
        assert dish.description == fixture_dish['description']
        assert str(dish.price) == fixture_dish['price']

        response_delete_dish = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        )
        assert response_delete_dish.status_code == HTTPStatus.OK

        dish_after_delete = db.query(Dishes).filter(Dishes.id == dish_id).first()
        assert dish_after_delete is None

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        response_delete_menu = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

    def test_update_dish(self, client, fixture_menu, fixture_submenu, fixture_dish, db: Session):
        response_create_menu = client.post('/api/v1/menus', json=fixture_menu)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=fixture_submenu
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        response_create_dish = client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
            json=fixture_dish,
        )
        assert response_create_dish.status_code == HTTPStatus.CREATED
        dish_id = str(response_create_dish.json()['id'])

        updated_data = {'title': 'Updated dish', 'description': 'Updated description', 'price': '2222.01'}
        response_update_dish = client.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            json=updated_data,
        )
        assert response_update_dish.status_code == HTTPStatus.OK
        assert response_update_dish.json()['title'] == updated_data['title']
        assert response_update_dish.json()['description'] == updated_data['description']
        assert response_update_dish.json()['price'] == str(updated_data['price'])

        dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
        assert dish is not None
        assert dish.title == updated_data['title']
        assert dish.description == updated_data['description']
        assert str(dish.price) == updated_data['price']

        response_delete_dish = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        )
        assert response_delete_dish.status_code == HTTPStatus.OK

        dish_after_delete = db.query(Dishes).filter(Dishes.id == dish_id).first()
        assert dish_after_delete is None

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        response_delete_menu = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

    def test_delete_dish(self, client, fixture_menu, fixture_submenu, fixture_dish, db: Session):
        response_create_menu = client.post('/api/v1/menus', json=fixture_menu)
        assert response_create_menu.status_code == HTTPStatus.CREATED
        menu_id = str(response_create_menu.json()['id'])

        response_create_submenu = client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=fixture_submenu
        )
        assert response_create_submenu.status_code == HTTPStatus.CREATED
        submenu_id = str(response_create_submenu.json()['id'])

        response_create_dish = client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
            json=fixture_dish,
        )
        assert response_create_dish.status_code == HTTPStatus.CREATED
        dish_id = str(response_create_dish.json()['id'])

        response_delete_dish = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        )
        assert response_delete_dish.status_code == HTTPStatus.OK

        dish_after_delete = db.query(Dishes).filter(Dishes.id == dish_id).first()
        assert dish_after_delete is None

        response_delete_submenu = client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        )
        assert response_delete_submenu.status_code == HTTPStatus.OK

        submenu_after_delete = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        assert submenu_after_delete is None

        response_delete_menu = client.delete(f'/api/v1/menus/{menu_id}')
        assert response_delete_menu.status_code == HTTPStatus.OK

        menu_after_delete = db.query(Menu).filter(Menu.id == menu_id).first()
        assert menu_after_delete is None