from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from db.mongo import Mongo_db, get_mongo_data
from models.like import Like
from services.token_authentication import (
    get_user_id_from_token,
)

router = APIRouter()


@router.post("/addlikefilm")
async def add_like_film(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    result = Like(user_id=user_id, movies_id=data["movies_id"], like=data["like"])
    await mongo_service.send_document(document=result.dict(), collection="likes")
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.get("/getlikebyfilm", response_model=list[Like])
async def get_like_by_film(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    s_filter = {"movies_id": data["movies_id"]}
    result = await mongo_service.get_aggregate_document(
        s_filter=s_filter, collection="likes"
    )

    result = [Like(**x) for x in result]
    return result


@router.get("/getlikebyuser", response_model=list[Like])
async def get_like_by_user(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    s_filter = {"user_id": user_id}
    result = await mongo_service.get_aggregate_document(
        s_filter=s_filter, collection="likes"
    )
    result = [Like(**x) for x in result]
    return result


@router.post("/addlikereviews")
async def add_like_reviews(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.delete("/dellike", response_model=list[Like])
async def del_like(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    await mongo_service.del_document(
        user_id=user_id, movies_id=movies_id, collection="likes"
    )

    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)
