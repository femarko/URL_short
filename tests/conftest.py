import pytest
from sqlalchemy.orm import clear_mappers

from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


@pytest.fixture(autouse=True, scope="session")
def mapp_tables():
    orm_conf.start_mapping()
    orm_conf.drop_tables()
    orm_conf.create_tables()
    yield
    orm_conf.drop_tables()
    clear_mappers()


