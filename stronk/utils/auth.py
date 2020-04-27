from firebase_admin import auth
from stronk.errors import errors as e


def verify_token(id_token):
    """Returns the uid for the user with id_token if id_token is valid and
       not revoked."""
    try:
        # Verify the ID token while checking if the token is revoked by
        # passing check_revoked=True.
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        # Token is valid and not revoked.
        return decoded_token['uid']
    except auth.RevokedIdTokenError:
        # Token revoked, inform the user to reauthenticate or signOut().
        raise e.RevokedIdTokenError("Token has been revoked.")
    except auth.InvalidIdTokenError:
        # Token is invalid
        raise e.InvalidIdTokenError("Token is not valid.")
