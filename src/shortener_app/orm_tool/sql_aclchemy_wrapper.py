from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, Any, Iterable, get_args, Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy import orm, Table, Column, Integer, String,DateTime, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.shortener_app.domain.models import URLShortened, DomainModel
from src.shortener_app.domain import errors as domain_errors
from src.config import settings


AsyncSessionType = Type[AsyncSession]


@dataclass
class ORMTool:
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

    def _init_table(self):
        for model in self.domain_models:
            columns = []
            for column_name, annotated_type in model.__annotations__.items():
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
            self.mappings |= {model: Table(model.__name__.lower(),
                                           self.table_mapper.metadata,
                                           *columns,
                                           extend_existing=True)}

    def start_mapping(self):
        if self._mapping_started:
            return
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError(message="No mappings provided.")
        for model, table in self.mappings.items():
            self.table_mapper.map_imperatively(class_=model, local_table=table)
        self._mapping_started = True

    async def create_tables(self):
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError(message="No mappings provided.")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.create_all)
        print(f"Tables created in the {settings.mode} database.")

    async def drop_tables(self):
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError("No mappings provided.")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.drop_all)
        print(f"Tables dropped in the {settings.mode} database.")

    async def reset_db(self):
        try:
            await self.drop_tables()
            await self.create_tables()
            print(f"The {settings.mode} database has been reset.")
        except Exception as e:
            raise domain_errors.DBError(message=f"Error during {settings.mode} database reset: {str(e)}")

    @staticmethod
    def clear_table_mappers():
        orm.clear_mappers()

    @staticmethod
    def sqlalch_select(*args, **kwargs):
        return select(*args, **kwargs)


def get_orm_tool(domain_models: Iterable[Type[DomainModel]], db_url: str = settings.db_url) -> ORMTool:
    return ORMTool(db_url=db_url, domain_models=domain_models)
