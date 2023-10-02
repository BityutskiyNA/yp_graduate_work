import datetime
from http import HTTPStatus

import redis
from config import config
from src.dataclasses.auth import AuthDataclass
from src.helpers.request_body import get_request_body

from flask import Blueprint, jsonify, request

REQUEST_LIMIT_PER_MINUTE = config.redisLB.REQUEST_LIMIT_PER_MINUTE

redis_conn = redis.Redis(
    host=config.redisLB.host, port=config.redisLB.port, db=config.redisLB.db
)


def request_limit(func):
    def wrapper(*args, **kwargs):
        body = get_request_body()
        auth_data = AuthDataclass(**body)
        pipe = redis_conn.pipeline()
        now = datetime.datetime.now()
        key = f"{auth_data.login}:{now.minute}"
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > REQUEST_LIMIT_PER_MINUTE:
            # return HTTPStatus.TOO_MANY_REQUESTS
            func(*args, **kwargs)
        else:
            func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
