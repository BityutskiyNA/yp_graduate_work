import uvicorn
from api.v1 import film_data
from config import config

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(film_data.router, prefix="/api/v1/film_data", tags=["film_data"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
    )
