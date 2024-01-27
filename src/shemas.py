from pydantic import BaseModel, UUID4
from uuid import UUID
from typing import Optional


class MenuIn(BaseModel):
    id: Optional[UUID4]
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class SubmenuIn(BaseModel):
    id: Optional[UUID4]
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class DishIn(BaseModel):
    id: Optional[UUID4]
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishOut(BaseModel):
    id: UUID4
    title: str
    description: str
    price: str
    submenu_id: UUID4

    class Config:
        orm_mode = True