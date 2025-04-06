import dataclasses
from typing import Type

from sqlalchemy import create_engine, orm
from sqlalchemy.exc import IntegrityError
from functools import lru_cache

from src.shortener_app.domain.models import DomainModel
from src.config import settings
from src.shortener_app.orm_tool.db_tables import DB_Table


table_mapper = orm.registry()


@dataclasses.dataclass
class ORMConf:
    def __init__(self):
        self.integrity_error = IntegrityError
        self.engine = create_engine(settings.db_url)
        self.session_maker = orm.sessionmaker(bind=self.engine)

    @staticmethod
    @lru_cache
    def start_mapping(*tables_to_map: tuple[Type[DomainModel], DB_Table]) -> None:
        for pair in tables_to_map:
            table_mapper.map_imperatively(class_=pair[0], local_table=pair[1])

    def create_tables(self) -> None:
        table_mapper.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        table_mapper.metadata.drop_all(bind=self.engine)


orm_conf = ORMConf()
