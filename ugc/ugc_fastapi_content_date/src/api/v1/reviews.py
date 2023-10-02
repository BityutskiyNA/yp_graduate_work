from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from db.mongo import Mongo_db, get_mongo_data
from models.reviews import Review
from services.token_authentication import (
    get_user_id_from_token,
)

router = APIRouter()


@router.post("/addreviews")
async def add_reviews(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    result = Review(
        user_id=user_id,
        movies_id=data["movies_id"],
        review_id=data["review_id"],
        review_text=data["review_text"],
    )
    await mongo_service.send_document(document=result.dict(), collection="reviews")
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)


@router.get("/getreviewsbyfilm", response_model=list[Review])
async def get_reviews_by_film(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    result = await mongo_service.get_aggregate_document_by_movie(
        movies_id=movies_id, collection="reviews"
    )
    result = [Review(**x) for x in result]
    return result


@router.get("/getreviewsbyuser", response_model=list[Review])
async def get_reviews_by_user(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
):
    result = await mongo_service.get_aggregate_document_by_user(
        user_id=user_id, collection="reviews"
    )
    result = [Review(**x) for x in result]
    return result


@router.delete("/delreview")
async def del_review(
    user_id: str = Depends(get_user_id_from_token),
    mongo_service: Mongo_db = Depends(get_mongo_data),
    data=Body(),
):
    movies_id = data["movies_id"]
    await mongo_service.del_document(
        user_id=user_id, movies_id=movies_id, collection="reviews"
    )
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.OK)
