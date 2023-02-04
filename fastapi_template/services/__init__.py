"""Services for fastapi_template."""
from fastapi_template.db.tortoise import UserRepository

from .auth import AuthService
from .user import UserService

__all__ = [
    "user_service",
    "auth_service",
]

user_service = UserService(user_repository=UserRepository())
auth_service = AuthService(user_service=user_service)
