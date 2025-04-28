from fastapi import APIRouter, HTTPException


healthcheck_route = APIRouter()


@healthcheck_route.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "OK"}
