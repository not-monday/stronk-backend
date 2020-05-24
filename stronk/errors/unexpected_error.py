from stronk import constants as c
from stronk.errors.base_exception import BaseException


class UnexpectedError(BaseException):

    def __init__(self, message, code=c.UNEXPECTED_ERROR_CODE):
        super().__init__(message, code)
