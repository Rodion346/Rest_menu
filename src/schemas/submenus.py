from pydantic import UUID4, BaseModel


class SubmenuIn(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4
    submenus_count: int | None
    dishes_count: int | None

    class Config:
        orm_mode = True
