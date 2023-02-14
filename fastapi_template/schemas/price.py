from typing import Union, List

from pydantic import Field, PositiveInt, PositiveFloat

from .base import BaseModel

__all__ = [
    'PriceFields',
    'BTC',
    'Price',
    'ReadPriceQuery',
]


class PriceFields:
    usdt = Field(description='Price USDT', example=1)
    rub = Field(description='Price RUB', example=1)


class BasePrice(BaseModel):
    """Base model for price."""


class BTC(BasePrice):
    USDT: Union[PositiveInt, PositiveFloat] = PriceFields.usdt
    RUB: Union[PositiveInt, PositiveFloat] = PriceFields.rub


class Price(BasePrice):
    BTC: BTC


# Query
class ReadPriceQuery(BasePrice):
    currencies: List[str] = ['usdt', 'rub', ]
