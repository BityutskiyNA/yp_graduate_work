import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import config
from api.v1 import likes, bookmarks, comments, reviews


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["bookmarks"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
    )
