from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeVar, Annotated
from typing_extensions import TypedDict


class DomainModelBase:
    pass


DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


@dataclass
class URLShortened(DomainModelBase):
    """
    :class:`URLShortened` - represents domain model of shortened url

    :ivar original_url: original url that was shortened
    :ivar short_url: shortened url
    :ivar id: unique id of shortened url
    :ivar save_date: date when shortened url was saved
    """
    original_url: Annotated[str, {"nullable": False}, {"unique": True}]  # type: ignore
    short_url: Annotated[str, {"nullable": False}]  # type: ignore
    id: Annotated[Optional[int], {"primary_key": True}, {"autoincrement": True}] = None  # type: ignore
    save_date: Annotated[Optional[datetime], {"nullable": False}, {"server_default": datetime.now}] = None #type: ignore


class URLShortenedDict(TypedDict, total=False):
    """
    :class:`URLShortenedDict` - represents shortened url as a dictionary

    :ivar id: unique id of shortened url
    :ivar original_url: original url that was shortened
    :ivar short_url: shortened url
    :ivar save_date: date when shortened url was saved
    """
    id: int
    original_url: str
    short_url: str
    save_date: datetime
