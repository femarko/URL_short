from pydantic import BaseModel, HttpUrl

"""
Schemas
=======

Defines Pydantic models used as request and response schemas
for the FastAPI endpoints in this application.

"""


class URL(BaseModel):
    url: HttpUrl


class CutUrlSuccess(BaseModel):
    id: int
    short_url: str


class Failure(BaseModel):
    message: str


class CutUrlFailure(Failure):
    original_url: str


class HealthCheck(BaseModel):
    status: str
