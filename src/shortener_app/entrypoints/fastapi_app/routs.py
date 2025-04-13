from fastapi import APIRouter, Response

from fastapi.responses import RedirectResponse, JSONResponse

import src.shortener_app.entrypoints.fastapi_app.schemas as schemas

from src.shortener_app.sevice_layer import app_manager
from src.shortener_app.sevice_layer.unit_of_work import UnitOfWork
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.domain import errors as domain_errors


url_shotter_routs = APIRouter()


@url_shotter_routs.post(
    path="/",
    status_code=201,
    response_model=schemas.CutUrlSuccess,
    summary="Shorten a url and save it in the database if it is not already exists.",
    tags=["Shorten url"],
    responses={
        200: {
            "model": schemas.CutUrlSuccess,
            "description": "A shortened url is created and returned, but not saved, because it is already exists in"
                           " the database."
        },
        201: {"model": schemas.CutUrlSuccess, "description": "A shortened url is created and saved in the database."},
        500: {"model": schemas.CutUrlFailure, "description": "Unexpected server error."}
    }
)
async def cut_url(original_url: schemas.URL, response: Response) -> schemas.CutUrlSuccess | JSONResponse:
    try:
        short_url: str = app_manager.cut_url(original_url=str(original_url.url))
        urls_instance_id, is_saved_to_db = await app_manager.save_urls(
            original_url=str(original_url.url),
            short_url=short_url,
            uow=UnitOfWork(session_maker=orm_conf.session_maker)
        )
        if not is_saved_to_db:
            response.status_code = 200
        return schemas.CutUrlSuccess(id=urls_instance_id, short_url=short_url)
    except domain_errors.UnexpectedError as e:
        error = schemas.CutUrlFailure(message=e.message, original_url=str(original_url.url))
        return JSONResponse(content=error.model_dump(), status_code=500)


@url_shotter_routs.get(
    path="/{shorten_url_id}",
    status_code=307,
    response_model=None,
    summary="Accepts the entry ID as a path parameter and redirects to the address set by original URL.",
    tags=["Redirect by ID"],
    responses={
        404: {"model": schemas.Failure, "description": "URL not found."},
        500: {"model": schemas.Failure, "description": "Unexpected server error."}
    }
)
async def get_original_url(shorten_url_id: int) -> RedirectResponse | JSONResponse:
    try:
        original_url = await app_manager.get_original_url(
            urls_instance_id=shorten_url_id, uow=UnitOfWork(session_maker=orm_conf.session_maker)
        )
        return RedirectResponse(url=original_url, status_code=307)
    except domain_errors.NotFoundError as e:
        error = schemas.Failure(message=e.message)
        return JSONResponse(content=error.model_dump(), status_code=404)
    except domain_errors.UnexpectedError as e:
        error = schemas.Failure(message=str(e))
        return JSONResponse(content=error.model_dump(), status_code=500)