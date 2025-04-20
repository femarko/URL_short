import uvicorn
from fastapi import FastAPI, Depends
from typing import Optional

from src.config import settings
from src.shortener_app.entrypoints.fastapi_app.routs import url_shotter_routs
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import ORMTool


def create_app(orm_tool: Optional[ORMTool] = None) -> FastAPI:
    if settings.mode == "test":
        app = FastAPI()
    else:
        app = FastAPI(dependencies=[Depends(orm_tool.start_mapping)])
    app.include_router(url_shotter_routs)
    return app


def run_app(app: FastAPI):
    if settings.mode in {"test", "dev"}:
        uvicorn.run(app=app, host="127.0.0.1", port=8080)
    else:
        uvicorn.run(app=app, host="0.0.0.0", port=8080)
