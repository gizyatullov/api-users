from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field, PositiveInt

from fastapi_template.pkg.models.base import BaseModel
from fastapi_template.pkg.models.types import EncryptedSecretBytes

__all__ = [
    "User",
    "UserFields",
    "CreateUserCommand",
    "ReadUserByIdQuery",
    "ReadUserByUserNameQuery",
    "UpdateUserCommand",
    "DeleteUserCommand",
    "ChangeUserPasswordCommand",
    "UserRole",
]


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


class UserFields:
    id = Field(description="User id.", example=2)
    username = Field(description="User Login", example="TestTest")
    password = Field(
        description="User password",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    old_password = Field(
        description="Old user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    new_password = Field(
        description="New user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    role_name = Field(
        description="User role.",
        example=UserRole.USER.value,
    )


class BaseUser(BaseModel):
    """Base model for user."""

    class Config:
        orm_mode = True


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name
    is_seller: bool
    btc_balance: Optional[float] = None
    btc_address: Optional[str] = None
    otp: Optional[str] = None
    city: Optional[str] = None
    avatar: Optional[str] = None
    created: datetime
    is_banned: bool
    user_ban_date: Optional[datetime] = None


# Commands.
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


class UpdateUserCommand(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    id: PositiveInt = UserFields.id
    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: EncryptedSecretBytes = UserFields.new_password


# Query
class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id
