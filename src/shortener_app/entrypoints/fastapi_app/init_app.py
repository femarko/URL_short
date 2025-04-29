from fastapi import FastAPI, Depends
from typing import Optional

from src.config import settings
from src.shortener_app.entrypoints.fastapi_app import main_router
from src.shortener_app.orm_tool.sql_alchemy_wrapper import ORMTool


def create_app(orm_tool: Optional[ORMTool] = None) -> FastAPI:
    """
    Creates a FastAPI app with a pre-configured router and ORM tool.

    Depends on the ``settings`` module for configuration.

    :param orm_tool: An optional instance of `ORMTool` to use for the app.
        If not provided, the app will use the default instance created by the
        `get_orm_tool()` function.
    :return: A FastAPI app with the pre-configured router and ORM tool.
    """
    if settings.mode == "test":
        app = FastAPI()
    else:
        app = FastAPI(dependencies=[Depends(orm_tool.start_mapping)])
    app.include_router(main_router)
    return app
