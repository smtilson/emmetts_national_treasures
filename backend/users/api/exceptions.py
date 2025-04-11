from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework.response import Response
from rest_framework import status
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")
    view = context.get("view")
    view_name = view.__class__.__name__ if view else "Unknown"

    error_display = (
        f"Exception in {view_name}: {str(exc)}\n"
        f"Request: {request.method} {request.path}\n"
        f"Traceback: {traceback.format_exc()}"
    )
    print(error_display)
    logger.error(error_display)

    # Remap AuthenticationFailed to 401
    if isinstance(exc, AuthenticationFailed):
        response.status_code = status.HTTP_401_UNAUTHORIZED
    # Remap NotAuthenticated to 401
    if isinstance(exc, NotAuthenticated):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
