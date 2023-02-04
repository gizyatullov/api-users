from typing import List

from fastapi_template import shemas
from fastapi_template.db.tortoise import UserRepository
from fastapi_template.pkg.pkg.exceptions.user import IncorrectOldPassword
from fastapi_template.pkg.pkg.password import password

__all__ = ["UserService"]


class UserService:
    repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def create_user(self, cmd: shemas.CreateUserCommand) -> shemas.User:
        cmd.password.crypt_password()
        return await self.repository.create(cmd=cmd)

    async def read_all_users(self) -> List[shemas.User]:
        return await self.repository.read_all()

    async def read_specific_user_by_username(
        self,
        query: shemas.ReadUserByUserNameQuery,
    ) -> shemas.User:
        return await self.repository.read_by_username(query=query)

    async def read_specific_user_by_id(
        self,
        query: shemas.ReadUserByIdQuery,
    ) -> shemas.User:
        return await self.repository.read(query=query)

    async def change_password(
        self,
        cmd: shemas.ChangeUserPasswordCommand,
    ) -> shemas.User:
        user = await self.repository.read(query=shemas.ReadUserByIdQuery(id=cmd.id))

        if not password.check_password(cmd.old_password, user.password):
            raise IncorrectOldPassword
        user.password = cmd.new_password
        user_migrate = user.migrate(shemas.UpdateUserCommand)
        user_migrate.password.crypt_password()
        return await self.repository.update(cmd=user_migrate)

    async def delete_specific_user(self, cmd: shemas.DeleteUserCommand) -> shemas.User:
        return await self.repository.delete(cmd=cmd)
