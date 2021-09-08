import json
from typing import List

import aioredis


class RedisMachine:
    def __init__(self, uri=""):
        self.redis = aioredis.from_url(
            uri or "redis://localhost",
            encoding="utf-8",
            decode_responses=True
        )

    async def get_data(self, user_id):
        async with self.redis.client() as con:
            data = await con.get(user_id)

        return data

    async def get_value(self, user_id, key):
        async with self.redis.client() as con:
            data = await con.get(user_id) or "{}"
            data = json.loads(data)

        return data.get(key)

    async def set_state(self, user_id: str, state: str):
        async with self.redis.client() as con:
            data = await con.get(user_id)
            data['state'] = state
            await con.set(user_id, data)

    async def update_data(self, user_id, **kwargs):
        async with self.redis.client() as con:
            data = await con.get(user_id) or "{}"
            data = json.loads(data)
            data = {**data, **kwargs}
            await con.set(user_id, json.dumps(data))
