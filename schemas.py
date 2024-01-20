from pydantic import BaseModel, UUID4
from typing import Optional


class MenuBase(BaseModel):
    title: str
    description: Optional[str]


class MenuCreate(MenuBase):
    pass


class MenuOut(MenuBase):
    id: UUID4
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: Optional[str]


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuOut(SubmenuBase):
    id: UUID4
    dishes_count: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    price: str
    description: Optional[str]


class DishCreate(DishBase):
    pass


class DishOut(DishBase):
    id: UUID4
    submenu_id: UUID4

    class Config:
        orm_mode = True