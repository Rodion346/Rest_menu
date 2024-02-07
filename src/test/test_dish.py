from decimal import Decimal
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.models.models import Submenu
from src.repositories.dishes import DishesRepository
from src.test.revers import reverse_operation


@pytest.fixture
def dish_data() -> dict[str, str]:
    return {'title': 'My dish', 'description': 'My description', 'price': '1111.01'}


class TestDish:
    def test_read_dishes(self, client: TestClient, create_submenu: Submenu) -> None:
        response_read_dishes = client.get(
            reverse_operation('read_dishes', menu_id=create_submenu.menu_id, submenu_id=create_submenu.id)
        )
        assert response_read_dishes.status_code == HTTPStatus.OK
        assert response_read_dishes.json() == []

    def test_create_dish(self, client: TestClient, create_submenu: Submenu, dish_data: dict[str, str]) -> None:
        response_create_dish = client.post(
            reverse_operation('create_dish', menu_id=create_submenu.menu_id, submenu_id=create_submenu.id), json=dish_data
        )
        assert response_create_dish.status_code == HTTPStatus.CREATED

        dish_id = (response_create_dish.json()['id'])
        dish = DishesRepository().read(dish_id)

        assert dish is not None
        assert dish.title == dish_data['title']
        assert dish.description == dish_data['description']
        assert dish.price == Decimal(dish_data['price'])

    def test_read_dish(self, client: TestClient, create_dish: list, create_submenu: Submenu) -> None:
        response_read = client.get(
            reverse_operation('read_dish',
                              menu_id=create_dish[0], submenu_id=create_dish[1].submenu_id, dish_id=create_dish[1].id)
        )
        assert response_read.status_code == HTTPStatus.OK
        assert response_read.json()['title'] == create_dish[1].title
        assert response_read.json()['description'] == create_dish[1].description

        dish = DishesRepository().read(create_dish[1].id)

        assert dish is not None
        assert dish.title == create_dish[1].title
        assert dish.description == create_dish[1].description
        assert dish.price == Decimal(create_dish[1].price)

    def test_update_dish(self, client: TestClient, create_dish: list, create_submenu: Submenu) -> None:
        updated_data = {'title': 'Updated dish', 'description': 'Updated description', 'price': '2222.01'}
        response_update_dish = client.patch(
            reverse_operation('update_dish',
                              menu_id=create_dish[0], submenu_id=create_dish[1].submenu_id, dish_id=create_dish[1].id),
            json=updated_data,
        )
        assert response_update_dish.status_code == HTTPStatus.OK

        dish = DishesRepository().read(create_dish[1].id)

        assert dish is not None
        assert dish.title == updated_data['title']
        assert dish.description == updated_data['description']
        assert Decimal(dish.price) == Decimal(updated_data['price'])

    def test_delete_dish(self, client: TestClient, create_dish: list, create_submenu: Submenu) -> None:
        response_delete_dish = client.delete(
            reverse_operation('delete_dish',
                              menu_id=create_dish[0], submenu_id=create_dish[1].submenu_id, dish_id=create_dish[1].id),
        )
        assert response_delete_dish.status_code == HTTPStatus.OK

        dish = DishesRepository().read(create_dish[1].id)
        assert dish is None
