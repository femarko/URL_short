import uvicorn
from fastapi import FastAPI


def run_app(app: FastAPI):
    uvicorn.run(app=app, host="0.0.0.0", port=8080)