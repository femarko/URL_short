from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app.schemas import URL
from src.shortener_app.sevice_layer import app_manager, unit_of_work
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


url_shotter_routs = APIRouter()


@url_shotter_routs.post("/cut_url")
def cut_url(original_url: URL) -> dict[str, int | str]:
    return app_manager.cut_url_and_save(
        original_url=original_url.url, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
    )


@url_shotter_routs.get("/original_url/{id}")
def get_original_url(id: int) -> str:
    return app_manager.get_original_url(
        urls_instance_id=id, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
    )
