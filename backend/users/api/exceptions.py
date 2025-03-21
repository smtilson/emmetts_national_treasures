from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # Remap AuthenticationFailed to 401
    if isinstance(exc, AuthenticationFailed):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    # Remap NotAuthenticated to 401
    if isinstance(exc, NotAuthenticated):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
