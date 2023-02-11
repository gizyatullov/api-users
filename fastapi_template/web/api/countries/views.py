from typing import List

from fastapi import APIRouter, status

from fastapi_template import schemas
from fastapi_template.services import country_service

__all__ = [
    'router',
]

router = APIRouter()


@router.get(
    '/',
    response_model=List[schemas.Country],
    status_code=status.HTTP_200_OK,
    description='Get all countries.',
)
async def read_all_countries():
    return await country_service.read_all_countries()


@router.get(
    '/{country_id:int}',
    response_model=schemas.Country,
    status_code=status.HTTP_200_OK,
    description='Read specific country.',
)
async def read_country(
    country_id: int = schemas.CountryFields.id,
):
    return await country_service.read_specific_country_by_id(
        query=schemas.ReadCountryByIdQuery(id=country_id),
    )


@router.get(
    '/{name:str}',
    response_model=schemas.Country,
    status_code=status.HTTP_200_OK,
    description='Read specific country by name.',
)
async def read_country(
    name: str = schemas.CountryFields.name,
):
    return await country_service.read_specific_country_by_name(
        query=schemas.ReadCountryByNameQuery(name=name),
    )
