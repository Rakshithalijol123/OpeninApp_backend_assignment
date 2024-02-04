from typing import Any, Callable, Dict

from fastapi import FastAPI

from src.models.exceptions import RFC7807ExceptionModel


def _patch_http_validation_error(
    fastapi_app: FastAPI, original_openapi_func: Callable[[], Dict[str, Any]]
) -> Callable[[], Dict[str, Any]]:
    """Patch OpenAPI schema to use problem details as per RFC7807 for exceptions
    Args:
        fastapi_app (FastAPI): FastAPI app object to be patched
        original_openapi_func (Callable[[], Dict[str, Any]]): Function returning original OpenAPI schema stored in the
            FastAPI app
    Returns:
        Callable[[], Dict[str, Any]]: Patched function returning modified OpenAPI schema
    """

    def _inject_model_schema():
        if fastapi_app.openapi_schema:
            return fastapi_app.openapi_schema
        fastapi_app.openapi_schema = original_openapi_func()
        model_schema = RFC7807ExceptionModel.schema()
        fastapi_app.openapi_schema.setdefault("components", {}).setdefault("schemas", {}).update(
            {
                model_schema["title"]: model_schema,
                "HTTPValidationError": {**model_schema, "title": "HTTPValidationError"},
            }
        )
        return fastapi_app.openapi_schema

    return _inject_model_schema


def setup_swagger_auth(
    app: FastAPI, original_openapi: Callable[[], Dict[str, Any]], auth_url: str
) -> Callable[[], Dict[str, Any]]:
    """This function can be used as a replacement for the default fastapi function that generates the openapi
    (aka swagger) definition json file. It adds bearer token authentication to the Swagger UI even though the
    endpoints do not directly implement this authentication mechanisms. This is useful when the authentication
    is handled by a reverse proxy like nginx and the swagger UI should still be able to make authenticated requests.
    Replace the openapi function of the fastapi app object with the result of this function:
    app.openapi = setup_swagger_auth(app, app.openapi)
    Args:
        app (FastAPI): The fastapi app object
        original_openapi (Callable[[], Dict[str, Any]]): The original app.openapi function which will be used to
            generate the base openapi.json
    Returns:
        Callable[[], Dict[str, Any]]: Function that should replace the original app.openapi
    """

    def inject_auth_to_swagger():
        if app.openapi_schema:
            return app.openapi_schema
        app.openapi_schema = original_openapi()
        app.openapi_schema["components"] = app.openapi_schema.get(
            "components", {})
        app.openapi_schema["components"]["securitySchemes"] = {
            "OAuth2": {
                "type": "oauth2",
                "description": (
                    "OAuth client credentials (username and password) are required. "
                ),
                "flows": {
                    "clientCredentials": {
                        "tokenUrl": auth_url,
                        "scopes": {},
                    }
                },
            }
        }
        app.openapi_schema["security"] = [{"OAuth2": []}]
        return app.openapi_schema

    return inject_auth_to_swagger
