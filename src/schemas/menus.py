from pydantic import UUID4, BaseModel


class MenuIn(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode: bool = True


class MenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int | None = None
    dishes_count: int | None = None

    class Config:
        orm_mode: bool = True
