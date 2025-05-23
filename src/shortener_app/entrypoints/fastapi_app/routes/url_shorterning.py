from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse, JSONResponse

import src.shortener_app.entrypoints.fastapi_app.schemas as schemas

from src.shortener_app.application import app_manager
from src.shortener_app.application.unit_of_work import UnitOfWork
from src.shortener_app.infrastructure.orm_tool.init_orm_tool import get_initialized_orm_tool
from src.shortener_app.domain import errors as domain_errors


orm_tool = get_initialized_orm_tool()
url_shotter_routes = APIRouter()


@url_shotter_routes.post(
    path="/",
    status_code=201,
    response_model=schemas.CutUrlSuccess,
    summary="Shorten the URL and save it in the database if it does not already exist.",
    tags=["URL shortening"],
    responses={
        200: {
            "model": schemas.CutUrlSuccess,
            "description": "A shortened url is created and returned, but not saved, because it already exists in"
                           " the database."
        },
        201: {"model": schemas.CutUrlSuccess, "description": "A shortened url is created and saved in the database."},
        500: {"model": schemas.CutUrlFailure, "description": "Unexpected server error."}
    }
)
async def cut_url(original_url: schemas.URL, response: Response) -> schemas.CutUrlSuccess | JSONResponse:
    """
    Shortens a given URL and saves it in the database if it does not already exist.

    **Parameters:**
    - `original_url` (schemas.URL): The original URL to be shortened.
    - `response` (Response): The response object to modify the status code if the URL already exists.

    **Returns:**
    - `schemas.CutUrlSuccess` or `JSONResponse`: A response containing the shortened URL and its ID, or an error message.

    **Raises:**
    - `domain_errors.UnexpectedError`: If an unexpected server error occurs.
    - `domain_errors.DBError`: If a database error occurs.
    """
    try:
        short_url: str = app_manager.cut_url(original_url=str(original_url.url))
        urls_instance_id, is_saved_to_db = await app_manager.save_urls(
            original_url=str(original_url.url),
            short_url=short_url,
            uow=UnitOfWork(session_maker=orm_tool.session_maker)
        )
        if not is_saved_to_db:
            response.status_code = 200
        return schemas.CutUrlSuccess(id=urls_instance_id, short_url=short_url)
    except (domain_errors.UnexpectedError, domain_errors.DBError) as e:
        error = schemas.CutUrlFailure(message=e.message, original_url=str(original_url.url))
        return JSONResponse(content=error.model_dump(), status_code=500)


@url_shotter_routes.get(
    path="/{shorten_url_id}",
    status_code=307,
    response_model=None,
    summary="Accepts the entry ID as a path parameter and redirects to the address set by the original URL.",
    tags=["URL shortening"],
    responses={
        404: {"model": schemas.Failure, "description": "URL not found."},
        500: {"model": schemas.Failure, "description": "Unexpected server error."}
    }
)
async def get_original_url(shorten_url_id: int) -> RedirectResponse | JSONResponse:
    """
    Accepts the entry ID as a path parameter and redirects to the address set by the original URL.

    **Parameters:**
    - `shorten_url_id` (int): The ID of the shortened URL to be redirected.

    **Returns:**
    - Redirects to the original URL, or returns an error message.

    **Raises:**
    - `domain_errors.UnexpectedError`: If an unexpected server error occurs.
    - `domain_errors.DBError`: If a database error occurs.
    """
    try:
        original_url = await app_manager.get_original_url(
            urls_instance_id=shorten_url_id, uow=UnitOfWork(session_maker=orm_tool.session_maker)
        )
        return RedirectResponse(url=original_url, status_code=307)
    except (domain_errors.NotFoundError, domain_errors.DBError) as e:
        error = schemas.Failure(message=e.message)
        return JSONResponse(content=error.model_dump(), status_code=404)
    except domain_errors.UnexpectedError as e:
        error = schemas.Failure(message=str(e))
        return JSONResponse(content=error.model_dump(), status_code=500)