import jwt
from config import config

from flask import request


def auth_required(roles: list[str], is_refresh: bool):
    def inner(fun):
        def wrapper(*args, **kwargs):
            try:
                token = request.headers["Authorization"].split(" ")[-1]
            except:
                raise ValueError("Invalid request header")
            try:
                current_user = jwt.decode(
                    token, config.jwt.secret_key, algorithms=["HS256"]
                )
            except jwt.exceptions.DecodeError as err:
                print(f"{err}, {type(err)}")
            if current_user["is_refresh"] & (not (is_refresh)):
                raise Exception("Wrong refresh token")
            else:
                if roles == [config.admin.admin_role]:
                    if current_user["is_admin"]:
                        current_user["access_token"] = token
                        return fun(current_user, *args, **kwargs)
                    else:
                        raise Exception("Wrong access")
                else:
                    current_user["access_token"] = token
                    return fun(current_user, *args, **kwargs)

        wrapper.__name__ = fun.__name__
        return wrapper

    return inner
