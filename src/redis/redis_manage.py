import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from redis import asyncio as aioredis  # type: ignore
from src.config import REDIS_HOST, REDIS_PORT


class RedisTools:
    redis_client: aioredis.StrictRedis = aioredis.StrictRedis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)

    async def set_params(self, key: Any, data: Any) -> None:
        data_str: str = json.dumps(jsonable_encoder(data))
        await self.redis_client.set(jsonable_encoder(key), data_str, ex=2000)

    async def get_params(self, key: Any) -> Any | None:
        data: bytes | None = await self.redis_client.get(jsonable_encoder(key))
        if data is None:
            return None
        return json.loads(jsonable_encoder(data))

    async def invalid(self, key: Any) -> None:
        key = str(key)
        if key is not None:
            await self.redis_client.delete(jsonable_encoder(key))

    async def invalid_menu(self, id: Any) -> None:
        id = str(id)
        s_list = await self.get_params('all_submenus')
        d_list = await self.get_params('all_dishes')
        s_list_str: str = jsonable_encoder(s_list)
        d_list_str: str = jsonable_encoder(d_list)
        if s_list_str is not None and s_list is not None:
            for submenu in s_list:
                if submenu.menu_id == id:
                    await self.redis_client.delete(str(submenu.id))
                    await self.invalid_lists(submenu.id, 'all_submenus')
                    if d_list_str is not None and d_list is not None:
                        for dish in d_list:
                            if dish.submenu_id == submenu.id:
                                await self.redis_client.delete(str(dish.id))
                                await self.invalid_lists(submenu.id, 'all_dishes')
        await self.redis_client.delete(str(id))

    async def invalid_submenu(self, id: Any) -> None:
        id = str(id)
        d_list = await self.get_params('all_dishes')
        if d_list is not None:
            for item in d_list:
                if str(item.submenu_id) == id:
                    await self.redis_client.delete(str(item.id))
                    await self.invalid_lists(item.id, 'all_dishes')
        await self.redis_client.delete(str(id))

    async def invalid_lists(self, ids: Any, key: str) -> None:
        ids = str(ids)
        lists_data: bytes | None = await self.redis_client.get(key)
        if lists_data is not None:
            lists = json.loads(lists_data)
            filtered_lists = [ent for ent in lists if ent.get('id') != ids]
            await self.redis_client.set(key, json.dumps(filtered_lists))

    async def count(self, id_ent) -> None:
        ent_d: bytes | None = await self.redis_client.get(str(id_ent))
        if ent_d is not None:
            lists_d = json.loads(ent_d)
            key = lists_d['menu_id']
            ent_ds: bytes | None = await self.redis_client.get(str(key))
            if ent_ds is not None:
                lists_d = json.loads(ent_ds)
                lists_d['submenus_count'] = 0
                lists_d['dishes_count'] = 0
                await self.redis_client.set(key, json.dumps(lists_d))
