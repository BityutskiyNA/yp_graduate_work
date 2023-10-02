from http import HTTPStatus

from src.decorators.auth import auth_required
from src.decorators.leakybucket import request_limit
from src.schemas.session import sessions_schema
from src.schemas.user import user_schema, users_schema
from src.services.session import session_service
from src.services.user import user_crud_service

from flask import Blueprint, jsonify, request

bp_admin_user = Blueprint("admin_user", __name__)


@bp_admin_user.route("/admin/user", methods=["POST"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def create_user(current_user):
    body = request.get_json(force=True)
    new_user = user_crud_service.create(data=body, roles=["user"])
    new_user_serialized = user_schema.dump(new_user)
    return jsonify(data=new_user_serialized, status=HTTPStatus.OK)


@bp_admin_user.route("/admin/user/<id>", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_user(current_user, id):
    user = user_crud_service.get_by_id(id)
    user_serialized = user_schema.dump(user)
    return jsonify(data=user_serialized, status=HTTPStatus.OK)


@bp_admin_user.route("/admin/user/<id>/sessions", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_user_sessions(current_user, id):
    user_sessions = session_service.get_by_user_id(id)
    user_sessions_serialized = sessions_schema.dump(user_sessions)
    return jsonify(data=user_sessions_serialized, status=HTTPStatus.OK)


@bp_admin_user.route("/admin/users", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_all_user(current_user):
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)
    users, count = user_crud_service.get_all(page, per_page)
    users_serialized = users_schema.dump(users)
    return jsonify(
        total=count,
        page=page,
        per_page=per_page,
        data=users_serialized,
        status=HTTPStatus.OK,
    )


@bp_admin_user.route("/admin/users/sessions", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_all_users_sessions(current_user):
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)
    user_sessions, count = session_service.get_all(page, per_page)
    user_sessions_serialized = sessions_schema.dump(user_sessions)
    return jsonify(
        total=count,
        page=page,
        per_page=per_page,
        data=user_sessions_serialized,
        status=HTTPStatus.OK,
    )


@bp_admin_user.route("/admin/user/<id>", methods=["PUT"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def update_user(current_user, id):
    body = request.get_json(force=True)
    user_crud_service.update_by_id(id, data=body)
    user = user_crud_service.get_by_id(id)
    user_serialized = user_schema.dump(user)
    return jsonify(data=user_serialized, status=HTTPStatus.OK)


@bp_admin_user.route("/admin/user/<id>", methods=["DELETE"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def delete_user(current_user, id):
    user = user_crud_service.get_by_id(id)
    user_serialized = user_schema.dump(user)
    user_crud_service.delete_by_id(id)
    return jsonify(data=user_serialized, status=HTTPStatus.OK)
