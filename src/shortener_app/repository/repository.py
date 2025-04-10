from datetime import datetime
from typing import Any, Protocol, Optional, cast, Type, Coroutine
from sqlalchemy import select

from src.shortener_app.domain.models import URLShortened
from sqlalchemy.ext.asyncio import AsyncSession

from src.shortener_app.domain.models import DomainModel


class NotFoundError(Exception):
    pass


class RepoProto(Protocol):
    async def add(self, instance) -> None: ...
    async def get(self, instance_id: int) -> DomainModel | None: ...
    async def find(self, **kwargs) -> DomainModel | None: ...
    async def delete(self, instance) -> None: ...



class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model_cl: Optional[Type[DomainModel]] = None

    async def add(self, instance) -> None:
        self.session.add(instance)

    async def get(self, instance_id: int) -> DomainModel | None:
        return await self.session.get(self.model_cl, instance_id)

    async def find(self, **kwargs) -> DomainModel | None:
        stmt = select(self.model_cl).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, instance) -> None:
        await self.session.delete(instance)


class URLRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)
        self.model_cl = URLShortened
