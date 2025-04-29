from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, Any, Iterable, get_args, Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy import orm, Table, Column, Integer, String,DateTime, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.shortener_app.domain.models import DomainModel
from src.shortener_app.domain import errors as domain_errors
from src.config import settings


AsyncSessionType = Type[AsyncSession]


@dataclass
class ORMTool:
    """
    :class:`ORMTool` - class for working with asynchronous SQLAlchemy ORM.

    This class provides methods for creating, dropping, and resetting the database, as well as mapping domain models
    to SQLAlchemy tables using imperative mapping in order to uncouple the domain models from the database.

    :ivar db_url: database connection url
    :ivar domain_models: list of domain models to be mapped
    :ivar engine: SQLAlchemy engine
    :ivar session_maker: session maker for creating new sessions
    :ivar integrity_error: exception class to be raised on integrity errors
    :ivar db_error: exception class to be raised on any other database errors
    :ivar mappings: dictionary mapping domain models to SQLAlchemy tables
    :ivar _mapping_started: flag indicating whether mapping has been started
    """
    db_url: str
    domain_models: Iterable[Type[DomainModel]]
    engine: AsyncEngine = field(init=False)
    session_maker: async_sessionmaker[AsyncSession] = field(init=False)
    integrity_error: Any = field(init=False, default=IntegrityError)
    db_error: Any = field(init=False, default=SQLAlchemyError)
    mappings: dict[Type[DomainModel], Table] = field(init=False, default_factory=dict)
    _mapping_started: bool = field(init=False, default=False)

    def __post_init__(self):
        """
        Initializes the ORMTool instance.

        This method is automatically called after the instance is created. It sets up the SQLAlchemy engine,
        session maker, table mapper, and type/value mappings for working with SQLAlchemy ORM.

        :ivar engine: The SQLAlchemy engine created using the database URL.
        :ivar session_maker: The session maker for creating new sessions with the engine.
        :ivar table_mapper: An ORM registry used for mapping domain models to tables.
        :ivar types_mapping: A dictionary mapping Python types to SQLAlchemy column types.
        :ivar values_mapping: A dictionary mapping Python functions to SQLAlchemy functions.
        :ivar _mapping_started: A flag indicating whether mapping has been started (initially set to False).
        """
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
        """
        Initializes the mappings of domain models to SQLAlchemy tables.

        This method iterates over the domain models and creates SQLAlchemy table columns based on the model's
        annotated fields. It sets up each table with the appropriate columns and adds the table to the `mappings`
        dictionary.

        :raises StopIteration: If no primary key column is found while organizing columns.
        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
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
        """
        Sets up the mappings of domain models to SQLAlchemy tables using imperative mapping in order to
        uncouple the domain models from the database.

        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
        if self._mapping_started:
            return
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError(message="No mappings provided.")
        for model, table in self.mappings.items():
            self.table_mapper.map_imperatively(class_=model, local_table=table)
        self._mapping_started = True

    async def create_tables(self):
        """
        Creates the database tables.

        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError(message="No mappings provided.")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.create_all)
        print(f"Tables created in the {settings.mode} database.")

    async def drop_tables(self):
        """
        Drops the database tables.

        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
        self._init_table()
        if not self.mappings:
            raise domain_errors.DBError("No mappings provided.")
        async with self.engine.begin() as conn:
            await conn.run_sync(self.table_mapper.metadata.drop_all)
        print(f"Tables dropped in the {settings.mode} database.")

    async def reset_db(self):
        """
        Resets the database by dropping all tables and creating them again.

        :raises domain_errors.DBError: If an error occurs during the process.
        """
        try:
            await self.drop_tables()
            await self.create_tables()
            print(f"The {settings.mode} database has been reset.")
        except Exception as e:
            raise domain_errors.DBError(message=f"Error during {settings.mode} database reset: {str(e)}")

    @staticmethod
    def clear_table_mappers():
        """
        Clears all table mappers.

        It is a static method and does not require an instance of the class to be called.

        :raises sqlalchemy.orm.exc.UnmappedClassError: If there are no mappers to clear.
        """
        orm.clear_mappers()

    @staticmethod
    def sql_select(*args, **kwargs):
        """
        Executes a SQLAlchemy select statement.

        :param args: Positional arguments for the select statement.
        :type args: tuple
        :param kwargs: Keyword arguments for the select statement.
        :type kwargs: dict
        :return: The select statement object.
        :rtype: sqlalchemy.sql.selectable.Select
        """
        return select(*args, **kwargs)


def get_orm_tool(domain_models: Iterable[Type[DomainModel]], db_url: str = settings.db_url) -> ORMTool:
    """
    Returns an instance of the `ORMTool` class.

    The `ORMTool` class implements the database operations.

    :param domain_models: An iterable of domain models.
    :type domain_models: Iterable[Type[DomainModel]]
    :param db_url: The URL of the database.
    :type db_url: str
    :return: The instance of the `ORMTool` class.
    :rtype: ORMTool
    """
    return ORMTool(db_url=db_url, domain_models=domain_models)
