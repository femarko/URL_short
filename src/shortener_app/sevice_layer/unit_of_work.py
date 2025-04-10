from typing import Callable, Protocol, Type

from sqlalchemy.ext.asyncio import AsyncSession

import src.shortener_app.domain.errors as domain_errors
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.repository.repository import URLRepository, RepoProto


class UnitOfWork:
    def __init__(self, session_maker: Callable[[], AsyncSession] = orm_conf.session_maker):
        self.session_maker = session_maker

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_maker()
        self.url_repo = URLRepository(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        try:
            await self.session.commit()
        except orm_conf.integrity_error:
            raise domain_errors.AlreadyExistsError
