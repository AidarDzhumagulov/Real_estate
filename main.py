from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middlewares.database_session import UniversalDBSessionMiddleware
from app.modules.users.views import user_router

middlewares = [
    # NOTE(axd1x8a): The order of middlewares is important
    # If you want to add new middleware, ask me first
    # or try to write it as ASGI middleware or else you will break whole app
    # good luck :)
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    ),
    Middleware(UniversalDBSessionMiddleware),
]


# API Endpoints
routes = [
    user_router,
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        middleware=middlewares,
        lifespan=lifespan,
        debug=settings.LOGLEVEL == "DEBUG",
    )
    for route in routes:
        app.include_router(route)
    return app


app = create_app()
