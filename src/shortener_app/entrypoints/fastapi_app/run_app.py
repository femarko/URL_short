import uvicorn
from fastapi import FastAPI

from src.config import settings


def run_app(app: FastAPI):
    # if settings.mode == "dev":
    #     uvicorn.run(app=app, host="127.0.0.1", port=8080)
    # else:
    #     uvicorn.run(app=app, host="0.0.0.0", port=8080)
    uvicorn.run(app=app, host="0.0.0.0", port=8080)