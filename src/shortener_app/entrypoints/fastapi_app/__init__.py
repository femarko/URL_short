from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app.routes.url_shorterning import url_shotter_routes
from src.shortener_app.entrypoints.fastapi_app.routes.healthcheck import healthcheck_route


main_router = APIRouter()
main_router.include_router(url_shotter_routes)
main_router.include_router(healthcheck_route, prefix="/check")
