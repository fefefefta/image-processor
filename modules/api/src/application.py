import os
import pathlib

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from db import DB_CONFIG
from api.endpoints import router
from api.redis_client import RedisJSONClient
from api.settings import Settings


settings = Settings()


def create_app() -> FastAPI:
    # Create Main FastAPI Application
    app = FastAPI(
        redoc_url=None,
        docs_url="/swagger/",
        title=settings.APP_NAME,
        # middleware=MIDDLEWARES,
    )

    # Include main router:
    app.include_router(prefix="/v1", router=router)

    # Create static folder if not exist:
    static_dir = os.path.join(settings.ROOT_DIR, "static")
    pathlib.Path(static_dir).mkdir(parents=True, exist_ok=True)
    app.mount(
        name="static",
        path="/static",
        app=StaticFiles(directory=static_dir),
    )

    @app.on_event("startup")
    async def startup_event():
        # Apply new migrations
        ...

        # Register redis client
        ...

    @app.on_event("shutdown")
    async def shutdown_event():
        # Close redis client
        ...

    return app
