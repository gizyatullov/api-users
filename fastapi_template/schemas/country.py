from typing import List, Union

from pydantic import Field, PositiveInt

from fastapi_template.pkg.types.strings import LowerStr
from .base import BaseModel
from .city import CityWithoutCountryID

__all__ = [
    'CountryFields',
    'Country',
    'ReadCountryByNameQuery',
    'ReadCountryByIdQuery',
    'ReadAllCountryQuery',
    'CountryWithCities',
]


class CountryFields:
    id = Field(description='Country id.', example=2)
    name = Field(description='Country name', example='russia')


class BaseCountry(BaseModel):
    """Base model for country."""

    class Config:
        orm_mode = True


class Country(BaseCountry):
    id: PositiveInt = CountryFields.id
    name: str = CountryFields.name


class CountryWithCities(Country):
    cities: Union[List[CityWithoutCountryID], List] = []


# Query
class ReadAllCountryQuery(BaseCountry):
    with_cities: bool = False


class ReadCountryByNameQuery(BaseCountry):
    name: LowerStr = CountryFields.name


class ReadCountryByIdQuery(BaseCountry):
    id: PositiveInt = CountryFields.id
