import os




"""
authentication middleware following wsgi
"""
class Middleware():
    #firebase service account config
    SERVICE_ACCOUNT_KEY = os.getenv('FIREBASE_SERVICE_ACCOUNT_CRED')

    def __init__(self, app):
        super().__init__()
        self.app = app

    def __call__(self, environ, start_response):
        # hardcoded for now
        authorized = True

        if (authorized):
            return self.app(environ, start_response)
        else:
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
