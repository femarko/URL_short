from typing import Any, Protocol, TypeVar, Generic, Mapping, Optional, ParamSpec
from datetime import datetime
from sqlalchemy import select
from typing_extensions import TypedDict, Unpack

from src.shortener_app.domain.models import URLShortened, URLShortenedDict, DomainModelBase
from src.shortener_app.domain import errors as domain_errors

from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


T = TypeVar("T")


class RepoProto(Protocol[T]):
    async def add(self, instance: T) -> None: ...
    async def get(self, instance_id: int) -> T | None: ...
    async def find(self, **kwargs: Unpack[dict[str, Any]]) -> T | None: ...
    async def delete(self, instance: T) -> None: ...


class Repository(Generic[T], RepoProto[T]):
    def __init__(self, session: orm_conf.asyncsession, model_cl: type[T]):
        self.session = session
        self.model_cl = model_cl

    async def add(self, instance: T) -> None:
        try:
            self.session.add(instance)
        except orm_conf.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def get(self, instance_id: int) -> T | None:
        try:
            return await self.session.get(self.model_cl, instance_id)
        except orm_conf.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def find(self, **kwargs: Unpack[URLShortenedDict]) -> T | None:  # type: ignore
        stmt = select(self.model_cl).filter_by()
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except orm_conf.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def delete(self, instance: T) -> None:
        try:
            await self.session.delete(instance)
        except orm_conf.db_error as e:
            raise domain_errors.DBError(message=str(e))


class URLRepository(Repository[URLShortened]):
    def __init__(self, session: orm_conf.asyncsession):
        super().__init__(session=session, model_cl=URLShortened)
