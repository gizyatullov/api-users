from fastapi.routing import APIRouter

from fastapi_template.web.api import (auth,
                                      docs,
                                      echo,
                                      monitoring,
                                      users,
                                      countries,
                                      cities,
                                      categories,
                                      subcategories,
                                      prices, )

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix='/echo', tags=['Echo'])
api_router.include_router(users.router, prefix='/user', tags=['User'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(countries.router, prefix='/country', tags=['Country'])
api_router.include_router(cities.router, prefix='/city', tags=['City'])
api_router.include_router(categories.router, prefix='/category', tags=['Category'])
api_router.include_router(subcategories.router, prefix='/subcategory',
                          tags=['Subcategory'])
api_router.include_router(prices.router, prefix='/price', tags=['Price'])
