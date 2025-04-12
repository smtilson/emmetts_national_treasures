from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    NotAuthenticated,
    ValidationError,
    APIException,
)
from rest_framework.response import Response
from rest_framework import status
import logging
import traceback
import json

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")
    view = context.get("view")
    view_name = view.__class__.__name__ if view else "Unknown"

    error_display = (
        f"Exception in {view_name}: {str(exc)}\n"
        f"Request: {request.method} {request.path}\n"
    )
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body_data = request.data
            error_display += f"\nRequest data: {json.dumps(body_data, default=str)}\n"
        except Exception as e:
            error_display += f"Failed to serialize request data: {str(e)}\n"
    error_display += f"Traceback: {traceback.format_exc()}\n"
    print(error_display)
    logger.error(error_display)

    if response is None:
        detail = str(exc)
        response = Response(
            {"detail": detail, "error_type": exc.__class__.__name__},
            status=status.HTTP_500_INTERNAL_ERROR,
        )

    # Process specific exception types
    if isinstance(exc, AuthenticationFailed) or isinstance(exc, NotAuthenticated):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        response.data = {
            "detail": str(exc.detail),
            "error_type": exc.__class__.__name__,
            "status_code": response.status_code,
        }
    elif isinstance(exc, ValidationError):
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.data = {
            "detail": "Request validation failed",
            "error_type": "ValidationError",
            "errors": exc.detail,
            "status_code": response.status_code,
        }
    elif hasattr(exc, "detail"):
        if isinstance(exc.detail, dict):
            response.data = {
                "detail": "Request validation failed",
                "error_type": exc.__class__.__name__,
                "errors": exc.detail,
                "status_code": response.status_code,
            }
        else:
            response.data = {
                "detail": str(exc.detail),
                "error_type": exc.__class__.__name__,
                "status_code": response.status_code,
            }

    return response
