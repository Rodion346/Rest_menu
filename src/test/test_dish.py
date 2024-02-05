from decimal import Decimal
from http import HTTPStatus
import pytest
from src.repositories.dishes import DishesRepository


@pytest.fixture
def dish_data():
    return {'title': 'My dish', 'description': 'My description', 'price': '1111.01'}


class TestDish:
    def test_read_dishes(self, client, create_submenu):
        response_read_dishes = client.get(
            f'/api/v1/menus/{create_submenu.menu_id}/submenus/{create_submenu.id}/dishes'
        )
        assert response_read_dishes.status_code == HTTPStatus.OK
        assert response_read_dishes.json() == []

    def test_create_dish(self, client, create_submenu, dish_data):
        response_create_dish = client.post(
            f'/api/v1/menus/{create_submenu.menu_id}/submenus/{create_submenu.id}/dishes', json=dish_data
        )
        assert response_create_dish.status_code == HTTPStatus.CREATED

        dish_id = str(response_create_dish.json()['id'])
        dish = DishesRepository().read(dish_id)

        assert dish is not None
        assert dish.title == dish_data['title']
        assert dish.description == dish_data['description']
        assert dish.price == Decimal(dish_data['price'])

    def test_read_dish(self, client, create_dish):
        response_read = client.get(
            f'/api/v1/menus/{create_dish[0]}/submenus/{create_dish[1].submenu_id}/dishes/{create_dish[1].id}'
        )
        assert response_read.status_code == HTTPStatus.OK
        assert response_read.json()['title'] == create_dish[1].title
        assert response_read.json()['description'] == create_dish[1].description

        dish = DishesRepository().read(create_dish[1].id)

        assert dish is not None
        assert dish.title == create_dish[1].title
        assert dish.description == create_dish[1].description
        assert dish.price == Decimal(create_dish[1].price)

    def test_update_dish(self, client, create_dish):
        updated_data = {'title': 'Updated dish', 'description': 'Updated description', 'price': '2222.01'}
        response_update_dish = client.patch(
            f'/api/v1/menus/{create_dish[0]}/submenus/{create_dish[1].submenu_id}/dishes/{create_dish[1].id}',
            json=updated_data,
        )
        assert response_update_dish.status_code == HTTPStatus.OK

        dish = DishesRepository().read(create_dish[1].id)

        assert dish is not None
        assert dish.title == updated_data['title']
        assert dish.description == updated_data['description']
        assert Decimal(dish.price) == Decimal(updated_data['price'])

    def test_delete_dish(self, client, create_dish):
        response_delete_dish = client.delete(
            f'/api/v1/menus/{create_dish[0]}/submenus/{create_dish[1].submenu_id}/dishes/{create_dish[1].id}',
        )
        assert response_delete_dish.status_code == HTTPStatus.OK

        dish = DishesRepository().read(create_dish[1].id)
        assert dish is None