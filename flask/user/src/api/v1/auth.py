from http import HTTPStatus

from src.dataclasses.auth import AuthDataclass
from src.decorators.auth import auth_required
from src.decorators.leakybucket import request_limit
from src.helpers.request_body import get_request_body
from src.helpers.request_user_agent import get_user_agent
from src.repositories.cache import cache_repository
from src.repositories.OAuth import OAuthSignIn
from src.services.role import role_crud_service
from src.services.session import session_service
from src.services.user import user_crud_service

from flask import Blueprint, jsonify, request

import requests
from datetime import datetime

bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/auth/register", methods=["POST"])
@request_limit
def register():
    body = get_request_body()
    auth_data = AuthDataclass(**body)
    role = role_crud_service.get_by_name("user")
    user_crud_service.create(
        {
            "login": auth_data.login,
            "password": auth_data.password,
            "email": auth_data.email,
        },
        roles=[role.name],
    )
    # отправка события при регистрации
    time_now = datetime.now()
    time_now_int = int(time_now.strftime("%Y%m%d"))

    session = requests.Session()
    session.trust_env = False

    redirect_url = "some_url"

    long_link = f"http://localhost:{auth_data.login}?redirect_url={redirect_url}?time={time_now_int}"
    try:
        response = session.post(
            "http://notifications_fastapi_api:8004/api/v1/notifications/send_to_queue_registration_event",
            json={"user_id": auth_data.login, "registration_link": long_link},
        )
    except Exception as e:
        pass
    return jsonify(msg="Registered successfully!", status=HTTPStatus.OK)


@bp_auth.route("/auth/login", methods=["POST"])
@request_limit
def login():
    body = get_request_body()
    auth_data = AuthDataclass(**body)
    auth_data.user_agent = get_user_agent()
    user = user_crud_service.get_by_login(auth_data.login)
    user_id = user.id
    cache_repository.check(user_id)
    access_token, refresh_token = session_service.create({"user_id": user_id, "user_agent": auth_data.user_agent})
    cache_repository.set(user_id, access_token)
    return jsonify(access_token=access_token, refresh_token=refresh_token, status=HTTPStatus.OK)


@bp_auth.route("/auth/logout", methods=["DELETE"])
@auth_required(roles=["admin", "user"], is_refresh=False)
@request_limit
def logout(current_user):
    session_service.deactivate_refresh(current_user["session_id"])
    cache_repository.block(current_user["user_id"])
    return jsonify(msg="Bye!", status=HTTPStatus.OK)


@bp_auth.route("/auth/login/Vkontakte", methods=["GET"])
@request_limit
def oauth_authorize():
    oauth = OAuthSignIn.get_provider("Vkontakte")
    return oauth.authorize()


@bp_auth.route("/auth/callback/Vkontakte", methods=["GET"])
def oauth_callback():
    oauth = OAuthSignIn.get_provider("Vkontakte")
    access_token = oauth.callback()

    try:
        user = user_crud_service.get_by_login(access_token["email"])
    except:
        body = {
            "login": access_token["email"],
            "email": access_token["email"],
            "password": access_token["email"],
            "social_id": access_token["user_id"],
        }
        auth_data = AuthDataclass(**body)
        role = role_crud_service.get_by_name("user")
        user_crud_service.create(
            {
                "login": auth_data.login,
                "password": auth_data.password,
                "email": access_token["email"],
                "social_id": access_token["user_id"],
            },
            roles=[role.name],
        )
        user = user_crud_service.get_by_login(access_token["email"])

    user_id = user.id
    cache_repository.check(user_id)
    access_token, refresh_token = session_service.create({"user_id": user_id, "user_agent": request.user_agent.string})
    cache_repository.set(user_id, access_token)
    return jsonify(access_token=access_token, refresh_token=refresh_token, status=HTTPStatus.OK)
