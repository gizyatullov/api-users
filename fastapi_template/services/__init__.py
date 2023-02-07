"""Services for fastapi_template."""
from fastapi_template.db.dao import user_repository

from .auth import AuthService
from .user import UserService

__all__ = [
    'user_service',
    'auth_service',
]

user_service = UserService(user_repository=user_repository)
auth_service = AuthService(user_service=user_service)
