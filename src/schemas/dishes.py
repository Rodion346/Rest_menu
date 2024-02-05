from pydantic import UUID4, BaseModel


class DishIn(BaseModel):
    id: UUID4 | None
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
