from fastapi import APIRouter

from fastapi.responses import RedirectResponse

from src.shortener_app.entrypoints.fastapi_app.schemas import URL
from src.shortener_app.sevice_layer import app_manager, unit_of_work
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


url_shotter_routs = APIRouter()


@url_shotter_routs.post("/", status_code=201)
def cut_url(original_url: URL) -> dict[str, int | str]:
    return app_manager.cut_url_and_save(
        original_url=original_url.url, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
    )


@url_shotter_routs.get(
    path="/{shorten_url_id}", responses={307: {"description": f"Temporary redirect to the original url"}}
)
def get_original_url(shorten_url_id: int) -> RedirectResponse:
    original_url = app_manager.get_original_url(
        urls_instance_id=shorten_url_id, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
    )
    return RedirectResponse(url=original_url, status_code=307)