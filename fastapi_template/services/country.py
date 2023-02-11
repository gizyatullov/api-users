from typing import List

from fastapi_template import schemas
from fastapi_template.db.dao import CountryDAO

__all__ = ['CountryService', ]


class CountryService:
    repository: CountryDAO

    def __init__(self, country_repository: CountryDAO):
        self.repository = country_repository

    async def read_all_countries(self) -> List[schemas.Country]:
        return await self.repository.read_all()

    async def read_specific_country_by_name(
        self,
        query: schemas.ReadCountryByNameQuery
    ) -> schemas.Country:
        return await self.repository.read_by_name(query=query)

    async def read_specific_country_by_id(
        self,
        query: schemas.ReadCountryByIdQuery,
    ) -> schemas.Country:
        return await self.repository.read(query=query)
