import json
from typing import Annotated, Union

import jwt
from jose import JWTError
from pydantic import BaseModel

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from config import config
from db.publish_to_kafka import KafkaPublisherAsync

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = config.jwt.secret_key
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[str, None] = None


class Film(BaseModel):
    id: str
    title: str


kafka_db = KafkaPublisherAsync()


@router.post("/addtorepository")
async def addtorepository(token: Annotated[str, Depends(oauth2_scheme)], data=Body()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        if data["id"] is None or data["event_time"] is None:
            return JSONResponse({"message": "not ok"}, status_code=400)
    except KeyError:
        return JSONResponse({"message": "not ok"}, status_code=400)

    message = {"user_id": user_id, "id": data["id"], "event_time": data["event_time"]}
    serialized_message = json.dumps(message).encode("utf-8")

    await kafka_db.connect()
    try:
        await kafka_db.send_message(message=serialized_message)
    finally:
        await kafka_db.disconnect()

    return JSONResponse({"message": "ok"}, status_code=200)
