from pydantic import Field, PositiveInt

from .base import BaseModel

__all__ = [
    'CountryFields',
    'Country',
    'ReadCountryByNameQuery',
    'ReadCountryByIdQuery',
]

from fastapi_template.pkg.types.strings import LowerStr


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


# Query
class ReadCountryByNameQuery(BaseCountry):
    name: LowerStr = CountryFields.name


class ReadCountryByIdQuery(BaseCountry):
    id: PositiveInt = CountryFields.id
