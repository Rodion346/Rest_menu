from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.db.database import get_async_session
from src.models.models import Menu, Submenu
from src.schemas.menus import MenuIn


class MenusRepository:
    model: type[Menu] = Menu

    async def read_all(self) -> Sequence[Menu]:
        async for session in get_async_session():
            query: Sequence[Menu] = (await session.execute(select(self.model))).scalars().all()
            return query
        assert False

    async def read_Dep(self):
        async for session in get_async_session():
            stmt = select(Menu).options(
                selectinload(Menu.submenus).selectinload(Submenu.dishes)
            )
            result = await session.execute(stmt)
            menus = result.scalars().all()
            menus_data = []
            for menu in menus:
                menu_data = {
                    'id': menu.id,
                    'title': menu.title,
                    'description': menu.description,
                    'submenus': [
                        {
                            'id': submenu.id,
                            'title': submenu.title,
                            'description': submenu.description,
                            'dishes': [
                                {
                                    'id': dish.id,
                                    'title': dish.title,
                                    'description': dish.description,
                                    'price': str(dish.price)
                                } for dish in submenu.dishes
                            ]
                        } for submenu in menu.submenus
                    ]
                }
                menus_data.append(menu_data)
            return menus_data

    async def read(self, id_ent: UUID) -> Any | None:
        async for session in get_async_session():
            query: Any | None = (
                await session.execute(
                    select(self.model)
                    .options(
                        joinedload(self.model.submenus)
                        .joinedload(Submenu.dishes)
                    )
                    .filter(self.model.id == id_ent)
                )
            ).scalars().first()
            if not query:
                return None

            query.submenus_count = len(query.submenus)
            query.dishes_count = sum(len(submenu.dishes) for submenu in query.submenus)
            return query
        assert False

    async def create(self, schemas: MenuIn) -> Any:
        async for session in get_async_session():
            stmt: Any = self.model(**schemas.dict())
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt

    async def update(self, id_ent: UUID, data: dict) -> Any | None:
        async for session in get_async_session():
            stmt: Any | None = ((
                await session.execute(
                    select(self.model).filter(self.model.id == id_ent))
            ).scalars().first())
            if stmt:
                for key, value in data.items():
                    setattr(stmt, key, value)
                await session.commit()
                await session.refresh(stmt)
                return stmt
        return None

    async def delete(self, id_ent: UUID) -> dict:
        async for session in get_async_session():
            stmt: Any | None = (
                await session.execute(
                    select(self.model).filter(self.model.id == id_ent))
            ).scalars().first()
            if stmt:
                await session.delete(stmt)
                await session.commit()
                return {'message': 'Menu and associated submenus deleted'}
        return {'message': f'No submenu found with id {id_ent}'}
