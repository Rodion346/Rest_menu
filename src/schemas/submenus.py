from pydantic import BaseModel, UUID4
from typing import Optional

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
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True