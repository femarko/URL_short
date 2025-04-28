from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app import schemas


healthcheck_route = APIRouter()


@healthcheck_route.get(
    "/health",
    tags=["Health check"],
    summary="Endpoint for the application's health check",
    response_model=schemas.HealthCheck
)
async def health_check() -> dict[str, str]:
    """
    Endpoint for the application's health check

    :return: Application status
    :rtype: dict[str, str]
    """
    return {"status": "OK"}
