from stronk import constants as c

class NotFound(Exception):
    status_code = 404

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message if message else c.NOT_FOUND_ERROR_MSG
        self.error_code = c.NOT_FOUND_ERROR_CODE
        self.status_code = status_code
