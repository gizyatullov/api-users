from fastapi.routing import APIRouter

from fastapi_template.web.api import auth, docs, echo, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix='/echo', tags=['Echo'])
api_router.include_router(users.router, prefix='/user', tags=['User'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
