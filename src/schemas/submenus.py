from pydantic import UUID4, BaseModel


class SubmenuIn(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode: bool = True


class SubmenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4
    dishes_count: int | None = None

    class Config:
        orm_mode: bool = True
