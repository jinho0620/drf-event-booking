from rest_framework.exceptions import APIException


class EventNotFoundException(APIException):
    status_code = 404
    default_detail = {"message": "해당 이벤트가 존재하지 않습니다."}