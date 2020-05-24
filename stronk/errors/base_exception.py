class BaseException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.context = {}
        if code:
            self.context['code'] = code
            self.context['message'] = message
