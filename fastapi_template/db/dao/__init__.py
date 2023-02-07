"""DAO classes."""
from .user import UserDAO

__all__ = [
    'UserDAO',
    'user_repository',
]

user_repository = UserDAO()
