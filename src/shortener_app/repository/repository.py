from typing import Any, Protocol, TypeVar, Generic
from sqlalchemy import select

from src.shortener_app.domain.models import URLShortened

from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


class NotFoundError(Exception):
    pass


T = TypeVar("T")


class RepoProto(Protocol[T]):
    async def add(self, instance: T) -> None: ...
    async def get(self, instance_id: int) -> T | None: ...
    async def find(self, **kwargs: dict[str, Any]) -> T | None: ...
    async def delete(self, instance: T) -> None: ...


class Repository(Generic[T], RepoProto[T]):
    def __init__(self, session: orm_conf.asyncsession, model_cl: type[T]):
        self.session = session
        self.model_cl = model_cl

    async def add(self, instance: T) -> None:
        self.session.add(instance)

    async def get(self, instance_id: int) -> T | None:
        return await self.session.get(self.model_cl, instance_id)

    async def find(self, **kwargs: dict[str, Any]) -> T | None:  # type: ignore
        stmt = select(self.model_cl).filter_by()
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)


class URLRepository(Repository[URLShortened]):
    def __init__(self, session: orm_conf.asyncsession):
        super().__init__(session=session, model_cl=URLShortened)
