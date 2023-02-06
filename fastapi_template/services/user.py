from typing import List

from fastapi_template import shemas
from fastapi_template.db.tortoise import UserRepository

__all__ = ['UserService']


class UserService:
    repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def create_user(self, cmd: shemas.CreateUserCommand) -> shemas.User:
        return await self.repository.create(cmd=cmd)

    async def read_all_users(self) -> List[shemas.User]:
        return await self.repository.read_all()

    async def read_specific_user_by_username(
        self,
        query: shemas.ReadUserByUserNameQuery,
        orm_obj: bool = False
    ):
        return await self.repository.read_by_username(query=query, orm_obj=orm_obj)

    async def read_specific_user_by_id(
        self,
        query: shemas.ReadUserByIdQuery,
    ) -> shemas.User:
        return await self.repository.read(query=query)

    async def change_password(
        self,
        cmd: shemas.ChangeUserPasswordCommand,
    ) -> shemas.User:
        return await self.repository.change_password(cmd=cmd)

    async def delete_specific_user(self, cmd: shemas.DeleteUserCommand) -> shemas.User:
        return await self.repository.delete(cmd=cmd)

    async def update_specific_user_by_username(self,
                                               cmd: shemas.UpdateUserCommand) -> shemas.User:
        return await self.repository.update_specific_user_by_username(cmd=cmd)
