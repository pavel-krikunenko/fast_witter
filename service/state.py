import asyncio

import asyncpg
from redis.asyncio.client import Redis


class State:
    def __init__(self, loop: asyncio.AbstractEventLoop, config: dict):
        self.loop = loop
        self.config = config
        self.db_pool: asyncpg.Pool = None
        self.redis: Redis = None