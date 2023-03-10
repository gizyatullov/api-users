from datetime import timedelta

from fastapi import APIRouter, status, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from redis.asyncio import ConnectionPool

from fastapi_template import schemas
from fastapi_template.services import auth_service
from fastapi_template.settings import settings
from fastapi_template.services.redis.dependency import get_redis_pool
from fastapi_template.web.api.exceptions.auth import IncorrectCaptcha

router = APIRouter()

__all__ = [
    'router',
]

access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRES)


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
    Authorize: AuthJWT = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    if not await auth_service.verify_captcha_in_redis(redis_pool=redis_pool,
                                                      uid_captcha=cmd.uid_captcha,
                                                      value_captcha=cmd.value_captcha):
        raise IncorrectCaptcha

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
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
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
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    Authorize.jwt_required()
    return Authorize.get_raw_jwt()


@router.post(
    '/captcha',
    response_model=schemas.CaptchaWithoutValue,
    status_code=status.HTTP_201_CREATED,
    description='Captcha.',
)
async def captcha(
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    return await auth_service.create_captcha(cmd=schemas.CaptchaQuery(),
                                             redis_pool=redis_pool)
