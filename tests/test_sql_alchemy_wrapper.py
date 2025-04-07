import pytest

from sqlalchemy.orm import clear_mappers
from sqlalchemy import text

from src.shortener_app.domain import models
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf, table_mapper


@pytest.fixture(autouse=True, scope="session")
def mapp_tables():
    orm_conf.start_mapping()
    yield
    clear_mappers()


def test_start_mapping():
    assert next(iter(table_mapper.mappers)).class_ == models.URLShortened


def test_create_table():
    orm_conf.create_tables()
    session = orm_conf.session_maker
    with session() as session:
        res = session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'url_shortened';")
        ).fetchall()
    assert res == [('url_shortened',)]
