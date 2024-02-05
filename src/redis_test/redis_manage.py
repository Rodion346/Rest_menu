import json

import redis  # type: ignore
from fastapi.encoders import jsonable_encoder

from src.config import REDIS_HOST, REDIS_PORT

redis_client = redis.StrictRedis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)


class RedisTools:
    redis_client: redis.StrictRedis = redis.StrictRedis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)

    def set_params(self, key, data):
        data_str = json.dumps(jsonable_encoder(data))
        self.redis_client.set(jsonable_encoder(key), data_str, ex=200)

    def get_params(self, key):
        data = self.redis_client.get(jsonable_encoder(key))
        if data is None:
            return None
        return json.loads(jsonable_encoder(data))

    def invalid(self, key):
        if key is not None:
            self.redis_client.flushdb()
