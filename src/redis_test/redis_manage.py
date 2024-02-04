import json
from fastapi.encoders import jsonable_encoder
import redis




redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class RedisTools:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set_params(self, key, data):
        redis_client.set(key, json.dumps(jsonable_encoder(data)))
