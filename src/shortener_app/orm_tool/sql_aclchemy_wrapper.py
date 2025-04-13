import dataclasses
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import orm, Table, Column, Integer, String,DateTime, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from functools import lru_cache

from src.shortener_app.domain.models import URLShortened
from src.config import settings


AsyncSessionType = Type[AsyncSession]

engine = create_async_engine(settings.db_url)
session_maker = async_sessionmaker(bind=engine)
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
    db_error = SQLAlchemyError
    asyncsession: AsyncSessionType = AsyncSession

    @staticmethod
    @lru_cache
    def start_mapping():
        table_mapper.map_imperatively(class_=URLShortened, local_table=url_shortened)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(table_mapper.metadata.create_all)
        print("Tables created.")

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(table_mapper.metadata.drop_all)
        print("Tables dropped.")

    async def reset_db(self):
        try:
            await self.drop_tables()
            await self.create_tables()
            print("Database reset.")
        except Exception as e:
            print(f"Error during DB reset: {str(e)}")


orm_conf = ORMConf()
