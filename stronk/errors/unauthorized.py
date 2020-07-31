from stronk import constants as c
from stronk.errors.base_exception import BaseException


class Unauthorized(BaseException):

    def __init__(self, message, code=c.UNAUTHORIZED_ERROR_CODE):
        super().__init__(message, code)
