from datetime import datetime
from typing import Optional


class URLShortened:
    def __init__(self,
                 original_url: str,
                 short_url: str,
                 id: Optional[int] = None,
                 save_date: Optional[datetime] = None):
        self.id = id
        self.original_url = original_url
        self.short_url = short_url
        self.save_date = save_date
