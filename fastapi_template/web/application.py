from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi_jwt_auth.exceptions import AuthJWTException

from fastapi_template.db.config import TORTOISE_CONFIG
from fastapi_template.logging import configure_logging
from fastapi_template.pkg.models.base import BaseAPIException
from fastapi_template.pkg.pkg.middlewares.handle_http_exceptions import (
    handle_api_exceptions,
    authjwt_exception_handler
)
from fastapi_template.settings import settings
from fastapi_template.web.api.router import api_router
from fastapi_template.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title=settings.API_INSTANCE_APP_NAME,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
        generate_schemas=True,
    )

    app.add_exception_handler(BaseAPIException, handle_api_exceptions)
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    return app
