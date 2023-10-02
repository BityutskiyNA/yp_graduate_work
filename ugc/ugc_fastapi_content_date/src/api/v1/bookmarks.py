from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from db.mongo import Mongo_db, get_mongo_data
from models.bookmark import Bookmark
from services.token_authentication import (
    get_user_id_from_token,
)

router = APIRouter()


@router.post("/addbookmarks")
async def add_bookmarks(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    valid_result = Bookmark(user_id=user_id, movies_id=data["movies_id"])
    await mongo_service.send_document(
        document=valid_result.dict(), collection="bookmarks"
    )
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.delete("/delbookmarks")
async def del_bookmarks(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    await mongo_service.del_document(
        user_id=user_id, movies_id=movies_id, collection="bookmarks"
    )
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.get("/bookmarkslist", response_model=list[Bookmark])
async def bookmarks_list(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
):

    result = await mongo_service.get_aggregate_document_by_user(
        user_id=user_id, collection="bookmarks"
    )
    result = [Bookmark(**x) for x in result]
    return result
