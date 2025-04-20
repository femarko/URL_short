from src.shortener_app.entrypoints.fastapi_app.init_app import create_app
from src.shortener_app.entrypoints.fastapi_app.run_app import run_app
from src.shortener_app.orm_tool.init_orm_tool import orm_tool


if __name__ == "__main__":
    run_app(app=create_app(orm_tool=orm_tool))
