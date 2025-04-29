from fastapi import APIRouter

from src.shortener_app.entrypoints.fastapi_app.routes.url_shorterning import url_shotter_routes
from src.shortener_app.entrypoints.fastapi_app.routes.healthcheck import healthcheck_route

"""
This module initializes and configures the main FastAPI router.

The router aggregates different API route modules, allowing for modular
and organized management of API endpoints.

Routes Included:
- URL Shortening: Handles operations related to URL shortening.
- Health Check: Provides an endpoint for checking the application's health status.
"""

main_router = APIRouter()
main_router.include_router(url_shotter_routes)
main_router.include_router(healthcheck_route, prefix="/check")
