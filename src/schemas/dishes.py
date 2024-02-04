from pydantic import BaseModel, UUID4
from typing import Optional

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