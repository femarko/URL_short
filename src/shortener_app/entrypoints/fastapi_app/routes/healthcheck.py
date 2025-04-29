from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app import schemas


healthcheck_route = APIRouter()


@healthcheck_route.get(
    "/health",
    tags=["Health check"],
    summary="Endpoint for the application's health check",
    response_model=schemas.HealthCheck
)
async def health_check() -> schemas.HealthCheck:
    """
    Endpoint for the application's health check.

    The response to this endpoint will always be a JSON object with a single key
    ``status`` with value ``"OK"``.

    :return: a JSON object with a single key ``status`` with value ``"OK"``
    """
    return schemas.HealthCheck(status="OK")
