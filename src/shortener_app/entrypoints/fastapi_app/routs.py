from typing import cast

from fastapi import APIRouter

from fastapi.responses import RedirectResponse

from src.shortener_app.entrypoints.fastapi_app.schemas import URL
from src.shortener_app.sevice_layer import app_manager
from src.shortener_app.sevice_layer.unit_of_work import UnitOfWork
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.domain import errors as domain_errors


url_shotter_routs = APIRouter()


@url_shotter_routs.post(path="/", status_code=201)
def cut_url(original_url: URL) -> dict[str, int | str]:
    short_url: str = app_manager.cut_url(original_url=str(original_url.url))
    entry_id: int = app_manager.save_urls(
        original_url=str(original_url.url), short_url=short_url, uow=UnitOfWork(session_maker=orm_conf.session_maker)
    )
    return {"id": entry_id, "short_url": short_url}


@url_shotter_routs.get(
    path="/{shorten_url_id}", responses={307: {"description": f"Temporary redirect to the original url"}}
)
def get_original_url(shorten_url_id: int) -> RedirectResponse:
    original_url = app_manager.get_original_url(
        urls_instance_id=shorten_url_id, uow=UnitOfWork(session_maker=orm_conf.session_maker)
    )
    return RedirectResponse(url=original_url, status_code=307)