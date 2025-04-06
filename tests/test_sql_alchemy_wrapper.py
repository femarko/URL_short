from src.shortener_app.domain import models
from src.shortener_app.orm_tool import db_tables
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf, table_mapper


def test_start_mapping():
    orm_conf.start_mapping((models.URLShortened, db_tables.url_shortened))
    assert next(iter(table_mapper.mappers)).class_ == models.URLShortened
