from stronk import app
from stronk import constants as c
from flask import jsonify


def default_body(status, code, msg):
    return {
        'status': status,
        'code': code,
        'message': msg
    }


def internal_server_error():
    status = 500
    body = default_body(status,
                        c.INTERNAL_SERVER_ERROR_CODE,
                        c.INTERNAL_SERVER_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp


def not_found_error(err):
    status = 404
    body = default_body(status,
                        c.NOT_FOUND_ERROR_CODE,
                        c.NOT_FOUND_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp


def bad_request():
    status = 400
    body = default_body(status,
                        c.BAD_REQUEST_ERROR_CODE,
                        c.BAD_REQUEST_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp


def conflict():
    status = 409
    body = default_body(status,
                        c.CONFLICT_ERROR_CODE,
                        c.CONFLICT_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp
