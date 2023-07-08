import asyncio

from fastapi import FastAPI, Depends
from misc.depends.session import get as get_session
from misc import (
    db,
    ctrl,
    redis
)
from misc.handlers import register_exception_handler
from models.base import ErrorResponse, UpdateErrorResponse
from service.routers import register_routers
from service.state import State
import logging

logger = logging.getLogger(__name__)

def create_app():
    app = ctrl.main_with_parses(None, main)
    if not app:
        raise RuntimeError
    return app


def main(args, config: dict) -> FastAPI:
    loop = asyncio.get_event_loop()
    state = State(loop, config)
    app = FastAPI(
        title="(Fast)witter API",
        debug=config.get('debug', False),
        root_path=config.get("root_path", None),
        responses=responses(),
        dependencies=[Depends(get_session)]
    )
    app.state = state
    state.app = app
    register_exception_handler(app)
    register_routers(app)
    register_shutdown(app)
    register_startup(app)
    return app


def register_shutdown(app: FastAPI):
    @app.on_event("shutdown")
    async def handler_shutdown():
        logger.info("Shutdown called")
        try:
            await shutdown(app)
        except:
            logger.exception("Shutdown crashed")

def register_startup(app: FastAPI):
    @app.on_event("startup")
    async def handler_startup():
        logger.info("Startup called")
        try:
            await startup(app)
        except:
            logger.exception("Startup crashed")


async def startup(app: FastAPI):
    app.state.db_pool = await db.init(app.state.config['db'])
    app.state.redis = await redis.init(app.state.config['redis'])


async def shutdown(app: FastAPI):
    if app.state.db_pool:
        await db.close(app.state.db_pool)
    if app.state.redis:
        await redis.close(app.state.redis)


def responses():
    return {
        409: {
            "model": UpdateErrorResponse
        },
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
