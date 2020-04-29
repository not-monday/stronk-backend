import unittest
from copy import deepcopy
from unittest.mock import patch, MagicMock

from flask import jsonify

from stronk import constants as c
from stronk.errors import handlers as h


class TestErrorResponse(unittest.TestCase):

    @patch("stronk.errors.handlers.jsonify")
    def test_happy_path(self, mock_jsonify):
        status_code = 123
        error_code = "error code"
        msg = "msg"
        body = deepcopy(c.ERROR_RESPONSE_BODY)
        body["code"] = error_code
        body["message"] = msg

        mock_jsonify.return_value = MagicMock(body)
        result = h.error_response(status_code, error_code, msg)

        mock_jsonify.assert_called_once_with(body)
        self.assertEqual(status_code, result.status_code, c.ASSERTION_ERROR_MSG.format(
            status_code, result.status_code))


class TestHandleHttpException(unittest.TestCase):
    returned = "returned"

    @patch("stronk.errors.handlers.handle_unexpected_errors")
    def test_unexpected_http_exception(self, mock_handle_unexpected_errors):
        error = MagicMock()
        error.name = "Random Exception"
        mock_handle_unexpected_errors.return_value = self.returned

        result = h.handle_http_exception(error)

        mock_handle_unexpected_errors.assert_called_once_with(error)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(self.returned,
                                                                result))

    @patch("stronk.errors.handlers.error_response")
    def test_bad_request(self, mock_error_response):
        error = MagicMock()
        error.code = 400
        error.name = "Bad Request"
        error.description = "Error description"
        mock_error_response.return_value = self.returned

        result = h.handle_http_exception(error)

        mock_error_response.assert_called_once_with(error.code,
                                                    c.BAD_REQUEST_ERROR_CODE,
                                                    error.description)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(self.returned,
                                                                result))

    @patch("stronk.errors.handlers.error_response")
    def test_conflict(self, mock_error_response):
        error = MagicMock()
        error.code = 409
        error.name = "Conflict"
        error.description = "Error description"
        mock_error_response.return_value = self.returned

        result = h.handle_http_exception(error)

        mock_error_response.assert_called_once_with(error.code,
                                                    c.CONFLICT_ERROR_CODE,
                                                    error.description)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(self.returned,
                                                                result))

    @patch("stronk.errors.handlers.error_response")
    def test_not_found(self, mock_error_response):
        error = MagicMock()
        error.code = 404
        error.name = "Not Found"
        error.description = "Error description"
        mock_error_response.return_value = self.returned

        result = h.handle_http_exception(error)

        mock_error_response.assert_called_once_with(error.code,
                                                    c.NOT_FOUND_ERROR_CODE,
                                                    error.description)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(self.returned,
                                                                result))

    @patch("stronk.errors.handlers.error_response")
    def test_unauthorized(self, mock_error_response):
        error = MagicMock()
        error.code = 401
        error.name = "Unauthorized"
        error.description = "Error description"
        mock_error_response.return_value = self.returned

        result = h.handle_http_exception(error)

        mock_error_response.assert_called_once_with(error.code,
                                                    c.UNAUTHORIZED_ERROR_CODE,
                                                    error.description)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(self.returned,
                                                                result))


class TestHandleUnexpectedErrors(unittest.TestCase):
    returned = "returned"

    @patch("stronk.errors.handlers.error_response")
    def test_happy_path(self, mock_error_response):
        mock_error_response.return_value = self.returned

        result = h.handle_unexpected_errors("")

        mock_error_response.assert_called_once_with(
            500, c.UNEXPECTED_ERROR_CODE, c.UNEXPECTED_ERROR_MSG)
        self.assertEqual(
            self.returned, result, c.ASSERTION_ERROR_MSG.format(True, result))
