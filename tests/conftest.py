import asyncio
from typing import Optional
from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.schema import CreateSchema

import app.database.session as database_session_mock_target
import app.middlewares.get_current_user as middleware_session_mock_target
import app.middlewares.request_logging as request_logging_mock_target
from app.config._settings import settings
from app.database.session import Base
from app.utils.dependencies import get_session
from main import app
from tests.fixtures import *  # noqa: F403


class AsyncTestDataAccessLayer:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.test_engine = create_async_engine(
            self.connection_url, execution_options={"isolation_level": "REPEATABLE READ"}
        )
        self.TestSession = async_sessionmaker(
            self.test_engine,
            class_=AsyncSession,  # type: ignore
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

    async def setup_database(self):
        async with self.test_engine.begin() as connection:
            await connection.run_sync(self.create_schema)
            await connection.run_sync(Base.metadata.create_all)  # type: ignore
        await self.test_engine.dispose()

    @staticmethod
    def create_schema(connection):
        inspector = inspect(connection)
        if "ditdemo" not in inspector.get_schema_names():
            connection.execute(CreateSchema("ditdemo"))


@pytest.fixture(scope="session")
async def async_DAL_fixture():
    connection_url = settings.DATABASE_TEST_URL
    test_dal = AsyncTestDataAccessLayer(connection_url)
    await test_dal.setup_database()
    return test_dal


@pytest.fixture
async def async_http_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture
def override_dependency(async_testing_session):
    app.dependency_overrides[get_session] = lambda: async_testing_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_testing_session(async_DAL_fixture: AsyncTestDataAccessLayer):
    session = async_DAL_fixture.TestSession
    async with session() as transaction:  # type: ignore
        try:
            yield transaction
            await transaction.commit()
        finally:
            await transaction.rollback()


@pytest.fixture(scope="session")
async def get_testing_session_manager_class(async_DAL_fixture):
    class SessionManagerTest:
        def __init__(self, session: Optional[AsyncSession] = None):
            self.session = session or async_DAL_fixture.TestSession()  # type: ignore
            self.autoclose = session is None

        async def __aenter__(self) -> AsyncSession:
            self.session = async_DAL_fixture.TestSession()
            return self.session

        async def __aexit__(self, exc_type, exc, tb):
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()

            if self.autoclose:
                await self.session.close()

    return SessionManagerTest


@pytest.fixture(scope="session")
async def mock_database_session(get_testing_session_manager_class):
    with patch.object(
        database_session_mock_target, "SessionManager", get_testing_session_manager_class
    ):
        yield


@pytest.fixture(scope="session")
async def mock_database_session_in_middlewares(get_testing_session_manager_class):
    with patch.object(
        middleware_session_mock_target,
        "SessionManager",
        get_testing_session_manager_class,
    ):
        yield


#
@pytest.fixture(scope="session")
async def mock_database_session_in_request_logging(get_testing_session_manager_class):
    with patch.object(
        request_logging_mock_target, "SessionManager", get_testing_session_manager_class
    ):
        yield
