from src.utils.repository import AbstractRepository
from src.schemas.dishes import DishIn


class DishesService:
    def __init__(self, dish_repo: AbstractRepository):
        self.dish_repo: AbstractRepository = dish_repo()

    def read_all(self):
        dish_list = self.dish_repo.read_all()
        return dish_list

    def read(self, id):
        dish = self.dish_repo.read(id)
        return dish

    def create(self, dish_in: DishIn, id):
        dish = self.dish_repo.create(dish_in, id)
        return dish

    def update(self, id, data):
        dish = self.dish_repo.update(id, data)
        return dish

    def delete(self, id):
        dish = self.dish_repo.delete(id)
        return dish