from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, Any, Iterable, get_args, Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy import orm, Table, Column, Integer, String,DateTime, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.shortener_app.domain.models import URLShortened, DomainModel
from src.config import settings


AsyncSessionType = Type[AsyncSession]


@dataclass
class ORMConf:
    db_url: str
    domain_models: Iterable[Type[DomainModel]]
    engine: AsyncEngine = field(init=False)
    session_maker: async_sessionmaker[AsyncSession] = field(init=False)
    integrity_error: Any = field(init=False, default=IntegrityError)
    db_error: Any = field(init=False, default=SQLAlchemyError)
    mappings: dict[Type[DomainModel], Table] = field(init=False, default_factory=dict)
    _mapping_started: bool = field(init=False, default=False)

    def __post_init__(self):
        self.engine = create_async_engine(self.db_url)
        self.session_maker = async_sessionmaker(bind=self.engine)
        self.table_mapper = orm.registry()
        self.types_mapping = {
            int: Integer,
            Optional[int]: Integer,
            str: String,
            datetime: DateTime,
            Optional[datetime]: DateTime
        }
        self.values_mapping = {datetime.now: func.now()}
        self._mapping_started = False

    def _init_table(self, domain: Type[DomainModel]):
        columns = []
        for column_name, annotated_type in domain.__annotations__.items():
            column_type, *kwargs_list = get_args(annotated_type)
            optional_params = {}
            for item in kwargs_list:
                for key, value in item.items():
                    optional_params |= {key: self.values_mapping.get(value, value)}
            columns.append(Column(column_name, self.types_mapping[column_type], **(optional_params or {})))
            first_column = filter(lambda column: column.primary_key, columns)
            try:
                columns = [columns.pop(columns.index(next(first_column))), *columns]
            except StopIteration:
                pass
        self.mappings |= {domain: Table(domain.__name__.lower(), self.table_mapper.metadata, *columns)}

    def start_mapping(self):
        if self._mapping_started:
            return
        for domain in self.domain_models:
            self._init_table(domain)
        for domain, table in self.mappings.items():
            self.table_mapper.map_imperatively(class_=domain, local_table=table)
        self._mapping_started = True

    async def create_tables(self):
        if not self.mappings:
            raise ValueError("No mappings provided.")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.create_all)
        print(f"Tables created in the {settings.mode} database.")

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.drop_all)
        print(f"Tables dropped in the {settings.mode} database.")

    async def reset_db(self):
        try:
            await self.drop_tables()
            await self.create_tables()
            print(f"The {settings.mode} database has been reset.")
        except Exception as e:
            print(f"Error during {settings.mode} database reset: {str(e)}")

    @staticmethod
    def sqlalch_select(*args, **kwargs):
        return select(*args, **kwargs)


orm_conf = ORMConf(db_url=settings.db_url, domain_models=(URLShortened,))
