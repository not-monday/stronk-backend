from firebase_admin import auth
from flask import request, g
from werkzeug import exceptions as e

from stronk.errors.unauthorized import Unauthorized
from stronk.constants import UNAUTHORIZED_ACTION_OR_RESOURCE_MSG


def verify_token():
    """Returns the uid of the user if their authorization token is valid and
       not revoked."""
    if request.endpoint == 'graphql':
        id_token = request.headers.get("Authorization")
        if not id_token:
            raise e.BadRequest("Missing Authorization token in header.")

        id_token = id_token.split()
        if len(id_token) != 2 or id_token[0] != "Bearer":
            raise e.BadRequest(
                "Authorization token in header has incorrect format.")

        id_token = id_token[1].strip()
        try:
            # Verify the ID token while checking if the token is revoked by
            # passing check_revoked=True.
            decoded_token = auth.verify_id_token(id_token, check_revoked=True)
            # Set the Firebase Token in the request context
            g.firebase_token = id_token
            g.id = decoded_token['uid']
        except auth.RevokedIdTokenError:
            # Token revoked, inform the user to reauthenticate or signOut().
            raise e.Unauthorized("Token has been revoked.")
        except auth.InvalidIdTokenError:
            # Token is invalid
            raise e.BadRequest("Token is not valid.")


def is_authorized(id: str):
    """Raises Unauthorized error if g.id (user's id) is not the same as id."""
    if not (id == g.id):
        raise Unauthorized(UNAUTHORIZED_ACTION_OR_RESOURCE_MSG)
