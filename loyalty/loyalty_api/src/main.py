import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio.client import Redis

from src.core.config import redis_settings
from src.db import redis
from src.api.v1 import loyalty_data

app = FastAPI(
    title="Loyalty API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.red.set_db(Redis(host=redis_settings.host, port=redis_settings.port))


@app.on_event("shutdown")
async def shutdown():
    await redis.red.db.close()


app.include_router(loyalty_data.router, prefix="/api/v1/loyalty", tags=["loyalty"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8006, reload=True  # "127.0.0.1 , 0.0.0.0"
    )
