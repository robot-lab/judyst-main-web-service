from rest_framework.response import Response


class ErrorResponse(object):
    def __init__(self):
        self.response = Response()

    def not_valid(self):
        self.response.status_code=400
        self.response.data = {"code": 400, "message": "invalid request"}
        return  self.response
