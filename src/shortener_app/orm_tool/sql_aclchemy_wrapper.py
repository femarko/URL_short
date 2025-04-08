import dataclasses

from sqlalchemy import create_engine, orm, Table, Column, Integer, String, DECIMAL,DateTime, func
from sqlalchemy.exc import IntegrityError
from functools import lru_cache

from src.shortener_app.domain.models import URLShortened
from src.config import settings


engine = create_engine(settings.db_url)
session_maker = orm.sessionmaker(bind=engine)
table_mapper = orm.registry()

url_shortened = Table(
    "url_shortened",
    table_mapper.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_url", String(500), nullable=False, unique=True),
    Column("short_url", String(35), nullable=False),
    Column("save_date", DateTime, server_default=func.now(), nullable=False)
)


@dataclasses.dataclass
class ORMConf:
    integrity_error = IntegrityError
    engine = engine
    session_maker = session_maker

    @staticmethod
    @lru_cache
    def start_mapping():
        table_mapper.map_imperatively(class_=URLShortened, local_table=url_shortened)

    def create_tables(self):
        table_mapper.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        table_mapper.metadata.drop_all(bind=self.engine)


orm_conf = ORMConf()
