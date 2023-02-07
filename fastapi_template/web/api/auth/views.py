from datetime import timedelta

from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth import AuthJWT

from fastapi_template import schemas
from fastapi_template.settings import settings
from fastapi_template.services import auth_service

router = APIRouter()

__all__ = [
    'router',
]

access_token_expires = timedelta(minutes=20)
refresh_token_expires = timedelta(days=30)


@AuthJWT.load_config
def get_config():
    return settings


@router.post(
    '/login',
    response_model=schemas.Auth,
    status_code=status.HTTP_200_OK,
    description='Route for authorize.',
)
async def auth_user(
    cmd: schemas.AuthCommand,
    Authorize: AuthJWT = Depends()
):
    user = await auth_service.check_user_password(cmd=cmd)

    access_token = Authorize.create_access_token(subject=user.username,
                                                 expires_time=access_token_expires)
    refresh_token = Authorize.create_refresh_token(subject=user.username,
                                                   expires_time=refresh_token_expires)
    return schemas.Auth(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    '/refresh',
    response_model=schemas.Auth,
    description='Get new tokens pair.',
)
async def create_new_token_pair(
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user,
                                                 expires_time=access_token_expires)
    refresh_token = Authorize.create_refresh_token(subject=current_user,
                                                   expires_time=refresh_token_expires)
    return schemas.Auth(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get(
    '/me',
)
async def get_me(
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    return Authorize.get_raw_jwt()
