from fastapi import APIRouter, FastAPI

from service.routers import auth, posts


def register_routers(app: FastAPI) -> FastAPI:
    router = APIRouter(
        prefix="/api/v1"
    )
    router.include_router(auth.router)
    router.include_router(posts.router)

    app.include_router(router)
    return app
