import pytest
from sqlalchemy import text


@pytest.mark.asyncio(loop_scope="session")
async def test_create_table(orm_test_tool):
    await orm_test_tool.create_tables()
    session = orm_test_tool.session_maker
    async with session() as session:
        cursor_result = await session.execute(
            text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'urlshortened');")
        )
        result = cursor_result.fetchone()[0]
    await orm_test_tool.drop_tables()
    assert result
