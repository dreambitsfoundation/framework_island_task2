from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status


class APIError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code = None, field=None):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            if field:
                self.detail = {field: force_str(detail)}
            else:
                self.detail = {"error": force_str(detail)}
        else: self.detail = {'detail': force_str(self.default_detail)}