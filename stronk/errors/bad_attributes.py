from stronk import constants as c
from stronk.errors.base_exception import BaseException


class BadAttributes(BaseException):

    def __init__(self, message, code=c.BAD_REQUEST_ERROR_CODE):
        super().__init__(message, code)
