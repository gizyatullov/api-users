"""DAO classes."""
from .user import UserDAO
from .country import CountryDAO
from .city import CityDAO

__all__ = [
    'UserDAO',
    'user_repository',
    'CountryDAO',
    'country_repository',
    'CityDAO',
    'city_repository',
]

user_repository = UserDAO()
country_repository = CountryDAO()
city_repository = CityDAO()
