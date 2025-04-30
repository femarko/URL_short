import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.shortener_app.domain.models import URLShortened
from src.shortener_app.infrastructure.orm_tool.sql_alchemy_wrapper import get_orm_tool
from src.shortener_app.entrypoints.fastapi_app.init_app import create_app


@pytest_asyncio.fixture
def orm_test_tool():
    orm_test_tool = get_orm_tool(db_url=settings.db_url, domain_models=(URLShortened,))
    return orm_test_tool


@pytest_asyncio.fixture(autouse=True)
async def mapp_tables(orm_test_tool):
    orm_test_tool.start_mapping()
    yield
    orm_test_tool.clear_table_mappers()


@pytest_asyncio.fixture
async def reset_db_fixture(orm_test_tool):
    await orm_test_tool.reset_db()
    yield
    await orm_test_tool.drop_tables()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
