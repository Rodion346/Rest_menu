from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select

from src.db.database import get_async_session
from src.models.models import Dishes
from src.schemas.dishes import DishIn


class DishesRepository:
    model: type[Dishes] = Dishes

    async def read_all(self) -> Sequence[Dishes]:
        async for session in get_async_session():
            query: Sequence[Dishes] = (await session.execute(select(self.model))).scalars().all()
            return query
        assert False

    async def read(self, id_ent: UUID, disc) -> Any | None:
        data = []
        async for session in get_async_session():
            query: Any | None = (
                await session.execute(
                    select(Dishes).filter(Dishes.id == id_ent))
            ).scalars().first()
            lists = disc
            if query is not None and query.manual_id is not None:
                data.append([query.manual_id, query.price])
                print(data)
                for check in lists['dishes']:
                    manual_id = f'{check[0]}:{check[1]}:{check[2]}'  # noqa: E231
                    disc = f'{check[3]}'
                    if data[0][0] == manual_id:
                        data[0][1] = int(data[0][1]) * (1 - int(disc) / 100)
                    query.price = data[0][1]
            return query
        assert False

    async def create(self, schemas: DishIn, submenu_id: UUID) -> Any:
        async for session in get_async_session():
            stmt: Any = self.model(**schemas.dict(), submenu_id=submenu_id)
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt

    async def update(self, id_ent: UUID, data: dict) -> Any | None:
        async for session in get_async_session():
            query: Any | None = (
                await session.execute(
                    select(self.model).filter(self.model.id == id_ent))
            ).scalars().first()
            if query:
                for key, value in data.items():
                    setattr(query, key, value)
                await session.commit()
                await session.refresh(query)
                return query
        return None

    async def delete(self, id_ent: UUID) -> dict:
        async for session in get_async_session():
            stmt: Any | None = (
                await session.execute(select(self.model).filter(self.model.id == id_ent))
            ).scalars().first()
            if stmt:
                await session.delete(stmt)
                await session.commit()
                return {'message': 'Menu and associated submenus deleted'}
        return {'message': f'No dish found with id {id_ent}'}
