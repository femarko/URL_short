from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeVar, Annotated
from typing_extensions import TypedDict


class DomainModelBase:
    pass


DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


@dataclass
class URLShortened(DomainModelBase):
    original_url: Annotated[str, {"nullable": False}, {"unique": True}]  # type: ignore
    short_url: Annotated[str, {"nullable": False}]  # type: ignore
    id: Annotated[Optional[int], {"primary_key": True}, {"autoincrement": True}] = None  # type: ignore
    save_date: Annotated[Optional[datetime], {"nullable": False}, {"server_default": datetime.now}] = None #type: ignore

    def get_params(self):
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_url": self.short_url,
            "save_date": self.save_date
        }


class URLShortenedDict(TypedDict, total=False):
    id: int
    original_url: str
    short_url: str
    save_date: datetime
