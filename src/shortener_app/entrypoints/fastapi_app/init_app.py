from fastapi import FastAPI, Depends
from typing import Optional

from src.config import settings
from src.shortener_app.entrypoints.fastapi_app import main_router
from src.shortener_app.entrypoints.fastapi_app.healthcheck_routes import healthcheck_route
from src.shortener_app.orm_tool.sql_alchemy_wrapper import ORMTool


def create_app(orm_tool: Optional[ORMTool] = None) -> FastAPI:
    if settings.mode == "test":
        app = FastAPI()
    else:
        app = FastAPI(dependencies=[Depends(orm_tool.start_mapping)])
    app.include_router(main_router)
    return app
