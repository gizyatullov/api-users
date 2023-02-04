from fastapi import APIRouter, Security, status
from fastapi_jwt import JwtAuthorizationCredentials

from fastapi_template import shemas
from fastapi_template.pkg.pkg import jwt
from fastapi_template.services import auth_service, user_service

router = APIRouter()

__all__ = [
    "router",
]


@router.post(
    "/login",
    response_model=shemas.Auth,
    status_code=status.HTTP_200_OK,
    description="Route for authorize.",
)
async def auth_user(
    cmd: shemas.AuthCommand,
):
    user = await auth_service.check_user_password(cmd=cmd)
    return jwt.jwt_service.get_token_pair(user=user)


@router.post(
    "/refresh",
    response_model=shemas.Auth,
    description="Get new tokens pair.",
)
async def create_new_token_pair(
    credentials: JwtAuthorizationCredentials = Security(jwt.refresh_security),
):
    user = await user_service.read_specific_user_by_username(
        query=shemas.ReadUserByUserNameQuery(username=credentials.jti),
    )
    return jwt.jwt_service.get_token_pair(user=user)


@router.get(
    "/me",
)
async def get_me(
    credentials: JwtAuthorizationCredentials = Security(jwt.access_security),
):
    return credentials
