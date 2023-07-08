import logging
import fastapi
from misc import db

logger = logging.getLogger(__name__)


async def get(request: fastapi.Request) -> db.Connection:
    try:
        pool = request.app.state.db_pool
    except AttributeError:
        raise RuntimeError("Db pool not found")
    else:
        async with pool.acquire() as conn:
            yield conn
