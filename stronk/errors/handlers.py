from copy import deepcopy

from flask import jsonify
from werkzeug.exceptions import HTTPException

from stronk import constants as c


def error_response(status_code, error_code, msg):
    body = deepcopy(c.ERROR_RESPONSE_BODY)
    body["code"] = error_code
    body["message"] = msg
    resp = jsonify(body)
    resp.status_code = status_code

    return resp


def handle_http_exception(e):
    """Error handler for HTTPExceptions."""
    exceptions_to_error_code = {
        'Bad Request': c.BAD_REQUEST_ERROR_CODE,
        'Conflict': c.CONFLICT_ERROR_CODE,
        'Not Found': c.NOT_FOUND_ERROR_CODE,
        'Unauthorized': c.UNAUTHORIZED_ERROR_CODE
    }
    name = e.name.strip()
    if name in exceptions_to_error_code:
        return error_response(e.code,
                              exceptions_to_error_code[name],
                              e.description)
    res = handle_unexpected_errors(e)
    return res


def handle_unexpected_errors(*_):
    """Error handler for generic exceptions."""
    return error_response(500,
                          c.UNEXPECTED_ERROR_CODE,
                          c.UNEXPECTED_ERROR_MSG)
