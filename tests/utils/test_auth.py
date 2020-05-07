import unittest
from unittest.mock import patch

from flask import request
from firebase_admin.auth import RevokedIdTokenError, InvalidIdTokenError, verify_id_token
from werkzeug import exceptions as e

from stronk.utils import auth
from tests import constants as test_c


@patch("stronk.utils.auth.current_app")
@patch("stronk.utils.auth.request")
class TestVerifyToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env = "development"
        cls.endpoint = "graphql"

    def test_not_graphql_endpoint(self, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = "endpoint"
        result = auth.verify_token()

        self.assertEqual(
            None, result, test_c.ASSERTION_ERROR_MSG.format(None, result))

    def test_not_prod_or_dev_env(self, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': 'testing'}
        mock_request.endpoint = self.endpoint
        result = auth.verify_token()

        self.assertEqual(
            None, result, test_c.ASSERTION_ERROR_MSG.format(None, result))

    @patch("stronk.utils.auth.g")
    @patch("stronk.utils.auth.auth.verify_id_token")
    def test_valid_token(self, mock_verify_id_token, mock_g, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = "Bearer id_token"
        mock_verify_id_token.return_value = {"uid": "id_token"}
        expected = "id_token"

        result = auth.verify_token()

        self.assertEqual(expected, result,
                         test_c.ASSERTION_ERROR_MSG.format(expected, result))

    def test_empty_auth_token(self, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = None
        with self.assertRaises(e.BadRequest) as context:
            auth.verify_token()

        self.assertTrue(
            "Missing Authorization token in header." in str(context.exception))

    def test_invalid_auth_token_format(self, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = "Bearer 1 2 3"
        with self.assertRaises(e.BadRequest) as context:
            auth.verify_token()

        self.assertTrue(
            "Authorization token in header has incorrect format." in str(context.exception))

    def test_invalid_auth_token_no_bearer(self, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = "123"
        with self.assertRaises(e.BadRequest) as context:
            auth.verify_token()

        self.assertTrue(
            "Authorization token in header has incorrect format." in str(context.exception))

    @patch("stronk.utils.auth.g")
    @patch("stronk.utils.auth.auth.verify_id_token")
    def test_revoked_id_token(self, mock_verify_id_token, mock_g, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = "Bearer id_token"
        mock_verify_id_token.side_effect = RevokedIdTokenError("Error")
        with self.assertRaises(e.Unauthorized) as context:
            auth.verify_token()

        self.assertTrue(
            "Token has been revoked." in str(context.exception))

    @patch("stronk.utils.auth.g")
    @patch("stronk.utils.auth.auth.verify_id_token")
    def test_invalid_id_token(self, mock_verify_id_token, mock_g, mock_request, mock_current_app):
        mock_current_app.config = {'ENV': self.env}
        mock_request.endpoint = self.endpoint
        mock_request.headers.get.return_value = "Bearer id_token"
        mock_verify_id_token.side_effect = InvalidIdTokenError("Error")
        with self.assertRaises(e.BadRequest) as context:
            auth.verify_token()

        self.assertTrue("Token is not valid." in str(context.exception))


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
