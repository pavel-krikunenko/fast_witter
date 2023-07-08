import asyncio
import os

import pytest
from asgi_lifespan import LifespanManager
from async_asgi_testclient import TestClient

from misc import db, conf as config
from misc.ctrl import CONFIG_ENV_KEY
from service.app import create_app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def app():
    instance = create_app()
    async with LifespanManager(instance):
        yield instance


@pytest.fixture(scope="session")
async def client(app):
    return TestClient(app)


@pytest.fixture(scope="session")
async def db_pool(app) -> db.Connection:
    return app.state.db_pool


@pytest.fixture(scope="session")
async def conf():
    config_path = os.environ[CONFIG_ENV_KEY]
    return config.read_config(config_path)


@pytest.fixture(scope="session")
async def resetdb(db_pool):
    await db_pool.execute('TRUNCATE users CASCADE')
    await db_pool.execute('TRUNCATE posts CASCADE')
