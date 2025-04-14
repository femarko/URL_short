from datetime import datetime
from typing import Optional, TypeVar
from typing_extensions import TypedDict


class DomainModelBase:
    pass


DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


class URLShortened(DomainModelBase):
    def __init__(self,
                 original_url: str,
                 short_url: str,
                 id: Optional[int] = None,
                 save_date: Optional[datetime] = None):
        self.id = id
        self.original_url = original_url
        self.short_url = short_url
        self.save_date = save_date

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
