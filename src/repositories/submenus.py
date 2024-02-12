from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import func, select

from src.db.database import get_async_session
from src.models.models import Dishes, Submenu
from src.schemas.submenus import SubmenuIn


class SubmenuRepository:
    model: type[Submenu] = Submenu

    async def read_all(self) -> Sequence[Submenu]:
        async for session in get_async_session():
            query: Sequence[Submenu] = (await session.execute(select(self.model))).scalars().all()
            return query
        assert False

    async def read(self, id_ent: UUID) -> Any | None:
        async for session in get_async_session():
            query: Any | None = (
                await session.execute(select(self.model).filter(self.model.id == id_ent))
            ).scalar_one_or_none()
            if not query:
                return None
            if query:
                d_count = (
                    await session.execute(
                        select(func.count(Dishes.id))
                        .join(self.model)
                        .filter(self.model.id == id_ent)
                    )
                ).scalar()
                query.dishes_count = d_count
                return query
        assert False

    async def create(self, schemas: SubmenuIn, menu_id: UUID) -> Any:
        async for session in get_async_session():
            stmt: Any = self.model(**schemas.dict(), menu_id=menu_id)
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt

    async def update(self, id_ent: UUID, data: dict) -> Any | None:
        async for session in get_async_session():
            stmt: Any | None = (
                await session.execute(
                    select(self.model).filter(self.model.id == id_ent))
            ).scalars().first()
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
                await session.execute(select(self.model).filter(self.model.id == id_ent))
            ).scalars().first()
            if stmt:
                await session.delete(stmt)
                await session.commit()
                return {'message': 'Menu and associated submenus deleted'}
        return {'message': f'No submenu found with id {id_ent}'}
