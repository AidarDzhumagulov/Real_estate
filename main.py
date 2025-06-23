from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middlewares.database_session import UniversalDBSessionMiddleware
from app.modules.users.views import user_router
from app.modules.listings.views import listing_router
from app.modules.attachments.views import attachment_router


origins = ["http://localhost:5173"]


middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(UniversalDBSessionMiddleware),
]


routes = [
    user_router,
    listing_router,
    attachment_router,
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
