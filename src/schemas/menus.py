from pydantic import UUID4, BaseModel


class MenuIn(BaseModel):
    id: UUID4 | None
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int | None
    dishes_count: int | None

    class Config:
        orm_mode = True
