from http import HTTPStatus

from src.decorators.auth import auth_required
from src.decorators.leakybucket import request_limit
from src.schemas.role import role_schema, roles_schema
from src.services.role import role_crud_service

from flask import Blueprint, jsonify, request

bp_admin_role = Blueprint("admin_role", __name__)


@bp_admin_role.route("/admin/role", methods=["POST"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def create_role(current_user):
    body = request.get_json(force=True)
    new_role = role_crud_service.create(data=body)
    new_role_serialized = role_schema.dump(new_role)
    return jsonify(data=new_role_serialized, status=HTTPStatus.OK)


@bp_admin_role.route("/admin/role/<id>", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_role(current_user, id):
    role = role_crud_service.get_by_id(id)
    role_serialized = role_schema.dump(role)
    return jsonify(data=role_serialized, status=HTTPStatus.OK)


@bp_admin_role.route("/admin/roles", methods=["GET"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def retrieve_all_roles(current_user):
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)
    roles, count = role_crud_service.get_all(page, per_page)
    roles_serialized = roles_schema.dump(roles)
    return jsonify(
        total=count,
        page=page,
        per_page=per_page,
        data=roles_serialized,
        status=HTTPStatus.OK,
    )


@bp_admin_role.route("/admin/role/<id>", methods=["PUT"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def update_role(current_user, id):
    body = request.get_json(force=True)
    role_crud_service.update_by_id(id, data=body)
    role = role_crud_service.get_by_id(id)
    role_serialized = role_schema.dump(role)
    return jsonify(data=role_serialized, status=HTTPStatus.OK)


@bp_admin_role.route("/admin/role/<id>", methods=["DELETE"])
@auth_required(roles=["admin"], is_refresh=False)
@request_limit
def delete_role(current_user, id):
    role = role_crud_service.get_by_id(id)
    role_serialized = role_schema.dump(role)
    role_crud_service.delete_by_id(id)
    return jsonify(data=role_serialized, status=HTTPStatus.OK)
