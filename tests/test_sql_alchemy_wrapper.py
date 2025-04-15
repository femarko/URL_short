from sqlalchemy import text

from src.shortener_app.domain import models
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf, table_mapper


def test_start_mapping():
    assert next(iter(table_mapper.mappers)).class_ == models.URLShortened


async def test_create_table():
    await orm_conf.create_tables()
    session = orm_conf.session_maker
    async with session() as session:
        cursor_result = await session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'url_shortened';")
        )
        result = cursor_result.fetchall()
    assert result == [('url_shortened',)]
