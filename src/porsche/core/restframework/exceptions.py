from rest_framework.exceptions import APIException

from porsche.core.exceptions import PorscheException
from porsche.models.enums import BusinessCode


class PorscheAPIException(APIException, PorscheException):
    business_code = BusinessCode.BAD_REQUEST
    message = "Api Exception"


class PorscheServerException(PorscheException):
    business_code = BusinessCode.SERVER_ERROR
    message = "Server Exception"
