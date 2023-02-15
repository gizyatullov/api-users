from typing import Dict

from redis.asyncio import ConnectionPool, Redis
import httpx

from fastapi_template import schemas
from fastapi_template.web.api.exceptions.price import ServiceIsUnavailable

__all__ = ['PriceService', ]


class PriceService:
    def _get_price_with_binance(self):
        ...

    def set_price_in_redis(self,
                           redis_pool: ConnectionPool) -> None:
        pass

    async def _read_price_in_redis(self,
                                   redis_pool: ConnectionPool,
                                   query: schemas.ReadPriceQuery) -> Dict[str, str]:
        result = {}
        async with Redis(connection_pool=redis_pool) as redis:
            for currency in query.currencies:
                v: bytes = await redis.get(name=f'price_{currency}')
                if v:
                    result[currency.upper()] = v.decode(encoding='utf-8')
                else:
                    raise ServiceIsUnavailable
        return result

    async def read_price(self,
                         query: schemas.ReadPriceQuery,
                         redis_pool: ConnectionPool) -> schemas.Price:
        prices = await self._read_price_in_redis(query=query, redis_pool=redis_pool)
        return schemas.Price(BTC=schemas.BTC(**prices))
