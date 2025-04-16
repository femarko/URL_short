from sqlalchemy import text

from src.shortener_app.domain import models
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf, table_mapper


async def test_create_table():
    await orm_conf.create_tables()
    session = orm_conf.session_maker
    async with session() as session:
        cursor_result = await session.execute(
            text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'url_shortened');")
        )
        result = cursor_result.fetchone()[0]
    assert result
