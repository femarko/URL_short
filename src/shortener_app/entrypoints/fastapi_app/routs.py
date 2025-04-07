from fastapi import APIRouter
from decimal import Decimal
from typing import cast

from src.shortener_app.entrypoints.fastapi_app.schemas import URL
from src.shortener_app.sevice_layer import app_manager, unit_of_work
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


url_shotter_routs = APIRouter()


@url_shotter_routs.post("/cut_url")
def cut_url(original_url: URL) -> dict[str, int | str]:
    result = app_manager.cut_url_and_save(original_url=original_url.url,
                                          uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker))
    return result


@url_shotter_routs.get("/get_info_from_db")
def get_info_from_db(number: int = 20,
                     page: int = 1,
                     per_page: int = 5) -> dict[str, int | list[dict[str, str |int | Decimal]]]:
    return app_manager.get_info_from_db(
        number=number, page=page, per_page=per_page, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
    )
