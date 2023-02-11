from typing import List, Union

from tortoise import models

from .base import BaseDAO
from fastapi_template import schemas
from fastapi_template.db.models.country import Country

__all__ = ['CountryDAO']


class CountryDAO(BaseDAO):
    def get_model(self) -> models.Model:
        return Country

    async def read(self,
                   query: schemas.ReadCountryByIdQuery,
                   orm_obj: bool = False) -> Union[schemas.Country, Country]:
        c = await Country.get(id=query.id)
        return c if orm_obj else schemas.Country.from_orm(c)

    async def read_by_name(self,
                           query: schemas.ReadCountryByNameQuery,
                           orm_obj: bool = False
                           ) -> Union[schemas.Country, Country]:
        c = await Country.get(name=query.name)
        return c if orm_obj else schemas.Country.from_orm(c)

    async def read_all(self) -> List[schemas.Country]:
        c = await Country.all()
        return [schemas.Country.from_orm(item) for item in c]
