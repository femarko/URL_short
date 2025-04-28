from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app.url_shorter_routes import url_shotter_routes
from src.shortener_app.entrypoints.fastapi_app.healthcheck_routes import healthcheck_route


main_router = APIRouter()
main_router.include_router(url_shotter_routes)
main_router.include_router(healthcheck_route, prefix="/check")
