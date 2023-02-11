"""Services for fastapi_template."""
from captcha.image import ImageCaptcha

from fastapi_template.db.dao import (user_repository,
                                     country_repository)
from .auth import AuthService
from .user import UserService
from .country import CountryService

__all__ = [
    'user_service',
    'auth_service',
    'country_service',
]

image_captcha = ImageCaptcha()

user_service = UserService(user_repository=user_repository)
auth_service = AuthService(user_service=user_service,
                           image_captcha=image_captcha)
country_service = CountryService(
    country_repository=country_repository
)
