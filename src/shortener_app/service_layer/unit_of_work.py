from typing import Callable

import src.shortener_app.domain.errors as domain_errors
from src.shortener_app.orm_tool.init_orm_tool import orm_tool
from src.shortener_app.repository.repository import URLRepository, RepoProto


class UnitOfWork:
    def __init__(self, session_maker: Callable = orm_tool.session_maker):
        self.session_maker = session_maker

    async def __aenter__(self) -> "UnitOfWork":
        self.session: orm_tool.asyncsession = self.session_maker()
        self.url_repo: RepoProto = URLRepository(session=self.session)
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
        except orm_tool.integrity_error:
            raise domain_errors.AlreadyExistsError

    async def flush(self):
        try:
            await self.session.flush()
        except orm_tool.integrity_error:
            raise domain_errors.AlreadyExistsError
