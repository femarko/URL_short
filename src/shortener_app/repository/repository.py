from typing import Any, Protocol, TypeVar, Generic
from typing_extensions import Unpack

from src.shortener_app.domain.models import URLShortened, URLShortenedDict
from src.shortener_app.domain import errors as domain_errors
from src.shortener_app.orm_tool.init_orm_tool import orm_tool


T = TypeVar("T")


class RepoProto(Protocol[T]):
    async def add(self, instance: T) -> None: ...
    async def get(self, instance_id: int) -> T | None: ...
    async def find(self, **kwargs: Unpack[dict[str, Any]]) -> T | None: ...
    async def delete(self, instance: T) -> None: ...


class Repository(Generic[T], RepoProto[T]):
    def __init__(self, session, db_error:orm_tool.db_error, select: orm_tool.sqlalch_select, model_cl: type[T]):
        self.session = session
        self.model_cl = model_cl
        self.db_error = db_error
        self.select = select

    async def add(self, instance: T) -> None:
        try:
            self.session.add(instance)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def get(self, instance_id: int) -> T | None:
        try:
            return await self.session.get(self.model_cl, instance_id)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def find(self, **kwargs: Unpack[URLShortenedDict]) -> T | None:  # type: ignore
        stmt = self.select(self.model_cl).filter_by(**kwargs)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def delete(self, instance: T) -> None:
        try:
            await self.session.delete(instance)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))


class URLRepository(Repository[URLShortened]):
    def __init__(self, session):
        super().__init__(
            session=session, model_cl=URLShortened, db_error=orm_tool.db_error, select=orm_tool.sqlalch_select
        )
