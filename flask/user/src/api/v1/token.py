from http import HTTPStatus

from src.decorators.auth import auth_required
from src.services.session import session_service

from flask import Blueprint, jsonify, request

bp_token = Blueprint("token", __name__)


@bp_token.route("/token/refresh", methods=["POST"])
@auth_required(roles=["admin", "user"], is_refresh=True)
def token_refresh(current_user):
    access_token, refresh_token = session_service.refresh_token(current_user["token"])
    session_service.deactivate_refresh(current_user["token"])
    return jsonify(
        access_token=access_token, refresh_token=refresh_token, status=HTTPStatus.OK
    )
