from http import HTTPStatus

from flask import Blueprint, jsonify, request
from src.services.user import user_crud_service
bp_notification = Blueprint("notification", __name__)


@bp_notification.route("/notification/getbyid/<id>", methods=["GET"])
def getbyid(id):
    user_obj = user_crud_service.get_by_id(id)
    data = {
        'fio': user_obj.fio,
        'time_zone': user_obj.time_zone,
        'email': user_obj.email,
    }
    if data:
        return jsonify(msg=data, status=HTTPStatus.OK)
    else:
        return jsonify(status=HTTPStatus.NOT_FOUND)


@bp_notification.route("/notification/getbytype/<type>", methods=["GET"])
def getbytype(type):
    user_objs = user_crud_service.get_by_type(type)
    data_list = []
    for user_obj in user_objs:
        data = {
            'fio': user_obj.fio,
            'time_zone': user_obj.time_zone,
            'email': user_obj.email,
        }
        data_list.append(data)
    if data:
        return jsonify(data_list, status=HTTPStatus.OK)
    else:
        return jsonify(status=HTTPStatus.NOT_FOUND)
