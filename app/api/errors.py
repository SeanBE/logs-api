class HTTPException(Exception):
    status = None
    msg = None

    def __init__(self, message=None):
        Exception.__init__(self)
        self.msg = message


class ResourceDoesNotExist(HTTPException):
    status = 404
