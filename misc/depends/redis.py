

from misc import redis
import logging
import fastapi
import asyncpg

logger = logging.getLogger(__name__)


async def get(request: fastapi.Request) -> redis.Connection:
    try:
        pool = request.app.state.redis
    except AttributeError:
        raise RuntimeError('Application state has no redis pool')
    else:
        async with await pool as conn:
            yield conn
