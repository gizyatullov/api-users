from datetime import timedelta

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from fastapi_template.settings import settings

from .credentionals import JwtService

__all__ = [
    "jwt_service",
]

access_security = JwtAccessBearer(
    secret_key=settings.JWT_SECRET_KEY.get_secret_value(),
    access_expires_delta=timedelta(minutes=20),
)
refresh_security = JwtRefreshBearer(
    secret_key=settings.JWT_SECRET_KEY.get_secret_value(),
    refresh_expires_delta=timedelta(days=30),
)
jwt_service = JwtService(
    access_security=access_security,
    refresh_security=refresh_security,
)
