import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import notifications_data

app = FastAPI(
    title="Notifications API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(
    notifications_data.router, prefix="/api/v1/notifications", tags=["notifications"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
    )
