from stronk import constants as c
from stronk.errors.base_exception import BaseException


class Conflict(BaseException):

    def __init__(self, message, code=c.CONFLICT_ERROR_CODE):
        super().__init__(message, code)
