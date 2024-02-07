import json
from typing import Any

from fastapi.encoders import jsonable_encoder

import redis  # type: ignore
from src.config import REDIS_HOST, REDIS_PORT
from src.models.models import Dishes, Submenu

redis_client: redis.StrictRedis = redis.StrictRedis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)


class RedisTools:
    redis_client: redis.StrictRedis = redis.StrictRedis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)

    def set_params(self, key: Any, data: Any) -> None:
        data_str: str = json.dumps(jsonable_encoder(data))
        self.redis_client.set(jsonable_encoder(key), data_str, ex=2000)

    def get_params(self, key: Any) -> Any | None:
        data: bytes | None = self.redis_client.get(jsonable_encoder(key))
        if data is None:
            return None
        return json.loads(jsonable_encoder(data))

    def invalid(self, key: Any) -> None:
        if key is not None:
            self.redis_client.delete(key)

    def invalid_menu(self, id: Any, s_list: list[Submenu], d_list: list[Dishes]) -> None:
        id = str(id)
        s_list_str: str = jsonable_encoder(s_list)
        d_list_str: str = jsonable_encoder(d_list)
        if s_list_str is not None:
            for submenu in s_list:
                if submenu.menu_id == id:
                    self.redis_client.delete(str(submenu.id))
                    if d_list_str is not None:
                        for dish in d_list:
                            if dish.submenu_id == submenu.id:
                                self.redis_client.delete(str(dish.id))
        self.redis_client.delete(str(id))

    def invalid_submenu(self, id: Any, d_list: list[Dishes]) -> None:
        id = str(id)
        for item in d_list:
            if str(item.submenu_id) == id:
                self.redis_client.delete(str(item.id))
                self.invalid_lists(item.id, 'all_dishes')
        self.redis_client.delete(str(id))

    def invalid_lists(self, ids: Any, key: str) -> None:
        ids = str(ids)
        lists_data: bytes | None = self.redis_client.get(key)
        if lists_data is not None:
            lists = json.loads(lists_data)
            filtered_lists = [ent for ent in lists if ent.get('id') != ids]
            self.redis_client.set(key, json.dumps(filtered_lists))

    def add_lists(self, key: str, data: dict) -> None:
        lists: bytes | None = self.redis_client.get(key)
        if lists is not None:
            ent: list[dict] = json.loads(lists.decode('utf-8'))
        else:
            ent = []
        ent.append(data)
        self.redis_client.set(key, json.dumps(jsonable_encoder(ent)))

    def add_count(self, key: str, id: Any, sub_id: Any | None = None) -> None:
        if key == 's':
            ent_s: bytes | None = redis_client.get(str(id))
            if ent_s is not None:
                lists = json.loads(ent_s)
                lists['submenus_count'] = len(json.loads(self.redis_client.get('all_submenus')))
                self.redis_client.set(id, json.dumps(lists))
        if key == 'd':
            ent_d: bytes | None = redis_client.get(str(id))
            ent_sub: bytes | None = redis_client.get(str(sub_id))
            if ent_d is None or ent_d == []:
                pass
            else:
                if ent_sub is None or ent_sub == []:
                    lists_d = json.loads(ent_d)
                    lists_d['submenus_count'] = 0
                    lists_d['dishes_count'] = 0
                    self.redis_client.set(id, json.dumps(lists_d))
                else:
                    lists_d = json.loads(ent_d)
                    lists_s = json.loads(ent_sub)
                    lists_d['dishes_count'] = len(json.loads(self.redis_client.get('all_dishes')))
                    lists_s['dishes_count'] = len(json.loads(self.redis_client.get('all_dishes')))
                    self.redis_client.set(sub_id, json.dumps(lists_s))
                    self.redis_client.set(id, json.dumps(lists_d))
