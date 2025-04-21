from fastapi import FastAPI, Depends
from typing import Optional

from src.config import settings
from src.shortener_app.entrypoints.fastapi_app.routes import url_shotter_routes
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import ORMTool


def create_app(orm_tool: Optional[ORMTool] = None) -> FastAPI:
    if settings.mode == "test":
        app = FastAPI()
    else:
        app = FastAPI(dependencies=[Depends(orm_tool.start_mapping)])
    app.include_router(url_shotter_routes)
    return app


