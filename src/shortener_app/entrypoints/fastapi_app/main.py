import uvicorn
from fastapi import FastAPI, Depends

from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.config import settings
from src.shortener_app.entrypoints.fastapi_app.routs import url_shotter_routs


app = FastAPI(dependencies=[Depends(orm_conf.start_mapping)])
app.include_router(url_shotter_routs)


def run_app():
    if settings.mode in {"test", "dev"}:
        uvicorn.run(app=app, host="127.0.0.1", port=8000)
    else:
        uvicorn.run(app=app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_app()
