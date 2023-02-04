from pydantic import Field

from fastapi_template.pkg.models.base import BaseModel
from fastapi_template.pkg.models.types import EncryptedSecretBytes, NotEmptySecretStr
from fastapi_template.shemas import UserFields

__all__ = ["Auth", "AuthCommand", "LogoutCommand"]


class AuthFields:
    access_token = Field(description="Bearer access token", example="exam.ple.token")
    refresh_token = Field(description="Bearer refresh token", example="exam.ple.token")
    fingerprint = Field(
        description="Unique fingerprint of user device",
        example="u-u-i-d",
    )
    role_name = UserFields.role_name
    username = UserFields.username
    password = UserFields.password


class BaseAuth(BaseModel):
    """Base model for auth."""


class Auth(BaseAuth):
    access_token: NotEmptySecretStr = AuthFields.access_token
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token


class AuthCommand(BaseAuth):
    username: str = AuthFields.username
    password: EncryptedSecretBytes = AuthFields.password


class LogoutCommand(BaseAuth):
    username: str = AuthFields.username
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token