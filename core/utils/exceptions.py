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
