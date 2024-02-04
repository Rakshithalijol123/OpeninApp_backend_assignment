from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status as http_resp_status
from starlette.exceptions import HTTPException as StarletteHTTPException


async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    return JSONResponse(content=exc.detail, status_code=exc.status_code, media_type="application/problem+json")


async def handle_unexpected_exception(request: Request, exc: Exception):
    return JSONResponse(
        content={
            "title": "Unexpected exception occurred",
            "detail": f"{type(exc).__name__}: {exc}",
            "status": http_resp_status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status_code=http_resp_status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/problem+json",
    )


async def handle_validation_exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={
            "title": "Validation Error",
            "detail": "Invalid endpoint input(s) detected",
            "status": http_resp_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error_specs": exc.errors(),
        },
        status_code=http_resp_status.HTTP_422_UNPROCESSABLE_ENTITY,
        media_type="application/problem+json",
    )
