"""Services for fastapi_template."""
from captcha.image import ImageCaptcha

from fastapi_template.db.dao import (user_repository,
                                     country_repository,
                                     city_repository, )
from .auth import AuthService
from .user import UserService
from .country import CountryService
from .city import CityService

__all__ = [
    'user_service',
    'auth_service',
    'country_service',
    'city_service',
]

image_captcha = ImageCaptcha()

user_service = UserService(user_repository=user_repository)
auth_service = AuthService(user_service=user_service,
                           image_captcha=image_captcha)
country_service = CountryService(
    country_repository=country_repository
)
city_service = CityService(
    city_repository=city_repository
)
