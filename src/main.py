from src.shortener_app.entrypoints.fastapi_app.init_app import create_app
from src.shortener_app.entrypoints.fastapi_app.run_app import run_app
from src.shortener_app.infrastructure.orm_tool.init_orm_tool import get_initialized_orm_tool

"""
Main entry point for the application.

The main entry point of the application is the :func:`run_app` function,
which is called with the result of the :func:`create_app` function.

The :func:`create_app` function creates a FastAPI app, and the
:func:`run_app` function runs the app with uvicorn.
"""

orm_tool = get_initialized_orm_tool()


if __name__ == "__main__":
    run_app(app=create_app(orm_tool=orm_tool))
