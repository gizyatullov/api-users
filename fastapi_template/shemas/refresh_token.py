from pydantic import PositiveInt

from fastapi_template.pkg.models.base import BaseModel
from fastapi_template.pkg.models.types import NotEmptySecretStr

__all__ = [
    "JWTRefreshToken",
    "CreateJWTRefreshTokenCommand",
    "ReadJWTRefreshTokenQuery",
    "ReadJWTRefreshTokenQueryByFingerprint",
    "UpdateJWTRefreshTokenCommand",
    "DeleteJWTRefreshTokenCommand",
]


class JWTFields:
    # user_id: PositiveInt =
    ...


class BaseJWTRefreshToken(BaseModel):
    """Base class for refresh token."""


class JWTRefreshToken(BaseJWTRefreshToken):
    """RefreshToken from database."""

    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


# Commands
class CreateJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


class UpdateJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


class DeleteJWTRefreshTokenCommand(BaseJWTRefreshToken):
    user_id: PositiveInt
    fingerprint: NotEmptySecretStr
    refresh_token: NotEmptySecretStr


# Queries
class ReadJWTRefreshTokenQuery(BaseJWTRefreshToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr


class ReadJWTRefreshTokenQueryByFingerprint(BaseJWTRefreshToken):
    user_id: PositiveInt
    fingerprint: NotEmptySecretStr
