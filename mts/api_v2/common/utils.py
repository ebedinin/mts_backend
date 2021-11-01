from rest_framework.views import exception_handler

from mts.api_v2.common.common import UNAUTHOROZED, TReturn


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code >= 400 & response.status_code < 500:
            rezult = TReturn()
            rezult.report.code = UNAUTHOROZED
            response.data = rezult.make()
            response.status_code = 200
    return response