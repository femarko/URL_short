from typing import TypeVar

from sqlalchemy import Table, Column, Integer, String, DateTime, func, orm as sqlalchemy_orm

DB_Table = TypeVar("DB_Table", bound=Table)

url_shortened = Table(
    "url_shortened",
    sqlalchemy_orm.registry().metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_url", String(500), nullable=False),
    Column("short_url", String(35), nullable=False),
    Column("save_date", DateTime, server_default=func.now(), nullable=False)
)
