from stronk import constants as c
from stronk.errors.base_exception import BaseException


class NotFound(BaseException):

    def __init__(self, message, code=c.NOT_FOUND_ERROR_CODE):
        super().__init__(message, code)
