import asyncio

import pytest
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from shop_list.db.base import Base
from shop_list.db.session import connection_string, engine
from shop_list.main import create_app
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database
from tests_helpers import common
from tests_helpers.factories import UserFactory

register(UserFactory)


@pytest.fixture(scope="session", autouse=True)
def sync_engine():
    new_connection_string = connection_string.replace("asyncpg", "psycopg2")
    engine = create_engine(new_connection_string)

    common.Session.configure(bind=engine)


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["pt_BR"]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_database_fixture():
    new_connection_string = connection_string.replace("asyncpg", "psycopg2")
    if not database_exists(new_connection_string):
        create_database(new_connection_string)
    yield
    drop_database(new_connection_string)


@pytest.mark.asyncio
@pytest.fixture(scope="session", autouse=True)
async def create_tables(create_database_fixture):
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def clear_database():
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def db_session(event_loop) -> AsyncSession:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
