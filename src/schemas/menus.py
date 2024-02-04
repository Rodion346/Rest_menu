from pydantic import BaseModel, UUID4
from typing import Optional


class MenuIn(BaseModel):
    id: Optional[UUID4]
    title: str
    description: str

    class Config:
        from_attributes = True


class MenuOut(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True