import json
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.db.redis import RedisManageData, get_redis_data
from src.models.loyalty import HistoryData
from src.db import db_service
from src.db.db_service import DateEncoder

router = APIRouter()


@router.get(
    "/get_all_promocodes",
    name="Получить все промокоды",
)
async def get_all_promocodes(
    db: Session = Depends(db_service.get_db),
    page: Annotated[int, Query(description="Pagination page number", ge=1)] = 1,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
) -> JSONResponse:
    promocodes = db_service.get_all_promocodes(db=db, limit=limit, page=page)

    if not promocodes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Promocodes not found"
        )
    json_data = json.dumps(promocodes, cls=DateEncoder)
    json_without_slash = json.loads(json_data)
    return JSONResponse(json_without_slash, status_code=HTTPStatus.OK)


@router.get(
    "/get_all_promocodes_by_campaign",
    name="Получить все промокоды по акции (промокампании)",
)
async def get_all_promocodes_by_campaign(
    campaign_id: str,
    db: Session = Depends(db_service.get_db),
    page: Annotated[int, Query(description="Pagination page number", ge=1)] = 1,
    limit: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
) -> JSONResponse:
    promocodes = db_service.get_all_promocodes_by_campaign(
        db=db, limit=limit, page=page, campaign_id=campaign_id
    )

    if not promocodes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Subscriptions not found"
        )
    json_data = json.dumps(promocodes, cls=DateEncoder)
    json_without_slash = json.loads(json_data)
    return JSONResponse(json_without_slash, status_code=HTTPStatus.OK)


@router.get(
    "/get_promo_info",
    name="Получить информацию об акции и промокоде",
)
async def get_promo_info(
    promocode: str,
    db: Session = Depends(db_service.get_db),
    redis: RedisManageData = Depends(get_redis_data),
) -> JSONResponse:
    promocode_check = await redis.get_data(promocode)

    if promocode_check:
        return JSONResponse(
            {"Message": "Promocode is in use"}, status_code=HTTPStatus.CONFLICT
        )
    info = db_service.get_campaign_info_by_promocode(db=db, promocode=promocode)

    if not info:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Campaign info not found"
        )
    if info["promocode_info"]["promo_code_type"] == "single_use":
        await redis.set_data(promocode, "in use")
    json_data = json.dumps(info, cls=DateEncoder)
    json_without_slash = json.loads(json_data)
    return JSONResponse(json_without_slash, status_code=HTTPStatus.OK)


@router.post(
    "/add_promocode_history", name="Запись в истории промокодов при успешной оплате"
)
async def add_promocode_history(
    history: HistoryData,
    db: Session = Depends(db_service.get_db),
    redis: RedisManageData = Depends(get_redis_data),
) -> JSONResponse:
    if history.status == "successful payment":
        promocode = db_service.get_promocode_info(
            promocode_id=history.promo_code_id, db=db
        )

        promocode_check = await redis.get_data(promocode.name)
        if promocode_check:
            if promocode.active:
                await redis.delete_data(promocode.name)
                try:
                    db_service.add_promocode_history(db=db, history=history)
                    result = db_service.set_promocode_used(
                        db=db, promocode_name=promocode.name
                    )
                except:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_REQUEST,
                        detail="Unable to add history",
                    )
                if result:
                    return JSONResponse(
                        {"status": "promocode marked as used"},
                        status_code=HTTPStatus.OK,
                    )
            else:
                await redis.delete_data(promocode.name)
                return JSONResponse(
                    {"status": "promocode already used"}, status_code=HTTPStatus.OK
                )
        return JSONResponse(
            {"status": "promocode was not requested yet"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
    return JSONResponse(
        {"status": "need status to be <successful payment>"},
        status_code=HTTPStatus.BAD_REQUEST,
    )
