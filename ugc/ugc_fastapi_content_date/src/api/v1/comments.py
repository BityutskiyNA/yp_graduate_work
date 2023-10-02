from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from db.mongo import Mongo_db, get_mongo_data
from models.comments import Сomment
from services.token_authentication import (
    get_user_id_from_token,
)

router = APIRouter()


@router.post("/addcomment")
async def add_comment(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    result = Сomment(
        user_id=user_id,
        movies_id=data["movies_id"],
        comment_id=data["comment_id"],
        comment_text=data["comment_text"],
    )
    await mongo_service.send_document(document=result.dict(), collection="comments")
    return JSONResponse({"message": "ok"}, atus_code=HTTPStatus.OK)


@router.delete("/delcomment")
async def del_comment(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    await mongo_service.del_document(
        user_id=user_id, movies_id=movies_id, collection="comments"
    )
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.get("/getcommentsbyfilm", response_model=list[Сomment])
async def get_comments_by_film(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    result = await mongo_service.get_aggregate_document_by_movie(
        movies_id=movies_id, collection="comments"
    )
    result = [Сomment(**x) for x in result]
    return result


@router.get("/getcommentsbyuser", response_model=list[Сomment])
async def get_comments_by_user(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
):
    result = await mongo_service.get_aggregate_document_by_user(
        user_id=user_id, collection="comments"
    )
    result = [Сomment(**x) for x in result]
    return result
