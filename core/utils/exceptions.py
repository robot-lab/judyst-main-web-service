from rest_framework.response import Response


# Error response code described in the technical specification.
class ErrorResponse(object):
    """class for error responses"""

    def __init__(self):
        self.response = Response()

    def not_valid(self):
        """not valid response 400"""
        self.response.status_code = 400
        self.response.data = {"code": 400, "message": "invalid request"}
        return self.response

    def user_exist(self):
        """user exist response 400"""
        self.response.status_code = 400
        self.response.data = {"code": 400, "message": "user already exist"}
        return self.response

    def not_found(self, data_caption="data"):
        """data not found response 404"""
        self.response.status_code = 404
        self.response.data = {"code": 404,
                              "message": f"{data_caption} not found"}
        return self.response


class CommonAnalysisException(Exception):
    def __init__(self, *args, **kwargs):
        if args.count > 0:
            self.message = args[0]
        if 'message' in kwargs:
            self.message = kwargs['message']
        if self.message is None:
            self.message = 'Error'

    def __str__(self):
        return self.message


class BadSearchRequestException(Exception):
    pass