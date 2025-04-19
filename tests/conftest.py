import asyncio

import pytest
import pytest_asyncio

from sqlalchemy.orm import clear_mappers
from fastapi.testclient import TestClient

from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.entrypoints.fastapi_app.main import app


@pytest_asyncio.fixture(autouse=True, scope="session")
async def mapp_tables():
    orm_conf.start_mapping()
    yield
    clear_mappers()


@pytest_asyncio.fixture
async def reset_db_fixture():
    await orm_conf.reset_db()
    yield
    await orm_conf.drop_tables()


@pytest_asyncio.fixture
async def client():
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True, scope="session")
def configure_asyncio_mode():
    policy = asyncio.get_event_loop_policy()
    asyncio.set_event_loop_policy(policy)