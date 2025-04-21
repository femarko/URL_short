from pydantic import BaseModel, HttpUrl


class URL(BaseModel):
    url: HttpUrl


class CutUrlSuccess(BaseModel):
    id: int
    short_url: str


class Failure(BaseModel):
    message: str


class CutUrlFailure(Failure):
    original_url: str

