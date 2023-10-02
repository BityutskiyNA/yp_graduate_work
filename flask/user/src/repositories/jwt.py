from datetime import datetime, timedelta

import jwt
from config import config
from src.dataclasses.payload import PayloadDataclass


class JWTRepository:
    def encode(self, payload: PayloadDataclass) -> dict:
        payload = (
            self._refresh(payload) if payload["is_refresh"] else self._access(payload)
        )
        token = jwt.encode(payload, config.jwt.secret_key, algorithm="HS256")
        return token

    def decode(self, token: str) -> str:
        return jwt.decode(token, config.jwt.secret_key, algorithms=["HS256"])

    def _access(self, payload):
        if payload["is_refresh"]:
            raise TypeError("Wrong token type")
        payload["exp"] = datetime.now() + timedelta(
            seconds=int(config.jwt.access_token_expires)
        )
        return payload

    def _refresh(self, payload):
        if not (payload["is_refresh"]):
            raise TypeError("Wrong token type")
        payload["exp"] = datetime.now() + timedelta(
            seconds=int(config.jwt.refresh_token_expires)
        )
        return payload
