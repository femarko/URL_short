from typing import cast

from fastapi import APIRouter

from fastapi.responses import RedirectResponse, JSONResponse

from src.shortener_app.entrypoints.fastapi_app.schemas import URL
from src.shortener_app.sevice_layer import app_manager
from src.shortener_app.sevice_layer.unit_of_work import UnitOfWork
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.domain import errors as domain_errors


url_shotter_routs = APIRouter()


@url_shotter_routs.post(path="/", status_code=201)
async def cut_url(original_url: URL) -> dict[str, int | str] | dict[str, str]:
    short_url: str = app_manager.cut_url(original_url=str(original_url.url))
    entry_id: int = await app_manager.save_urls(original_url=str(original_url.url), short_url=short_url,
                                                uow=UnitOfWork(session_maker=orm_conf.session_maker))
    return {"id": entry_id, "short_url": short_url}


@url_shotter_routs.get(path="/{shorten_url_id}", status_code=307, response_model=None)
async def get_original_url(shorten_url_id: int) -> RedirectResponse | JSONResponse:
    try:
        original_url = await app_manager.get_original_url(
            urls_instance_id=shorten_url_id, uow=UnitOfWork(session_maker=orm_conf.session_maker)
        )
        return RedirectResponse(url=original_url, status_code=307)
    except domain_errors.NotFoundError as e:
        return JSONResponse(content=e.message, status_code=404)