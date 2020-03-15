from stronk import app
from stronk import constants as c
from flask import jsonify
from stronk.errors.classes.notFound import NotFound

def default_body(status, code, msg):
    return {
        'status': status,
        'code': code,
        'message': msg
    }

@app.errorhandler(500)
def internal_server_error():
    status = 500
    body = default_body(status,
                        c.INTERNAL_SERVER_ERROR_CODE,
                        c.INTERNAL_SERVER_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp

@app.errorhandler(NotFound)
def not_found_error(err):
    body = default_body(err.status,
                        err.error_code,
                        err.message)
    resp = jsonify(body)
    resp.status_code = status

    return resp

@app.errorhandler(400)
def bad_request():
    status = 400
    body = default_body(status,
                        c.BAD_REQUEST_ERROR_CODE,
                        c.BAD_REQUEST_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp

@app.errorhandler(409)
def conflict():
    status = 409
    body = default_body(status,
                        c.CONFLICT_ERROR_CODE,
                        c.CONFLICT_ERROR_MSG)
    resp = jsonify(body)
    resp.status_code = status

    return resp