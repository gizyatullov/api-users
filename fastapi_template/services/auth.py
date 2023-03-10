import base64
import string
import random
from uuid import uuid4

from captcha.image import ImageCaptcha
from redis.asyncio import ConnectionPool, Redis

from fastapi_template import schemas
from fastapi_template.settings import settings
from fastapi_template.pkg.types.strings import NotEmptyStr
from fastapi_template.web.api.exceptions.auth import IncorrectUsernameOrPassword
from fastapi_template.services.user import UserService


class AuthService:
    user_service: UserService
    image_captcha: ImageCaptcha

    symbols: str = f'{string.digits}{string.ascii_lowercase}'

    def __init__(
        self,
        user_service: UserService,
        image_captcha: ImageCaptcha,
    ):
        self.user_service = user_service
        self.image_captcha = image_captcha

    async def check_user_password(self, cmd: schemas.AuthCommand) -> schemas.User:
        user = await self.user_service.read_specific_user_by_username(
            query=schemas.ReadUserByUserNameQuery(username=cmd.username),
            orm_obj=True
        )
        if not user or not await user.check_password(password=cmd.password):
            raise IncorrectUsernameOrPassword

        return schemas.User.from_orm(obj=user)

    async def _get_image_captcha(self, value: NotEmptyStr) -> bytes:
        return self.image_captcha.generate(chars=value).read()

    async def _gen_random_string(self) -> NotEmptyStr:
        random_characters: list = random.choices(self.symbols,
                                                 k=settings.CAPTCHA_NUMBER_CHARACTERS)
        return NotEmptyStr(''.join(random_characters))

    async def _bytes_per_base64_string(self, b: bytes) -> str:
        return base64.b64encode(s=b).decode(encoding='utf-8')

    @staticmethod
    async def verify_captcha_in_redis(redis_pool: ConnectionPool,
                                      uid_captcha: str,
                                      value_captcha: str) -> bool:
        async with Redis(connection_pool=redis_pool) as redis:
            v: bytes = await redis.get(name=f'captcha_{uid_captcha}')

        return value_captcha == v.decode(encoding='utf-8') if v else False

    @staticmethod
    async def _register_captcha_in_redis(redis_pool: ConnectionPool,
                                         uid_captcha: str,
                                         value_captcha: str):
        async with Redis(connection_pool=redis_pool) as redis:
            await redis.set(name=f'captcha_{uid_captcha}',
                            value=value_captcha,
                            ex=settings.CAPTCHA_TTL)

    async def create_captcha(self,
                             cmd: schemas.CaptchaQuery,
                             redis_pool: ConnectionPool) -> schemas.CaptchaWithoutValue:
        uid = uuid4()
        value = await self._gen_random_string()
        image = await self._get_image_captcha(value=value)
        image_in_base64 = await self._bytes_per_base64_string(b=image)
        await self._register_captcha_in_redis(redis_pool=redis_pool,
                                              uid_captcha=str(uid),
                                              value_captcha=value)
        return schemas.CaptchaWithoutValue(
            uid=uid,
            image=image_in_base64
        )
