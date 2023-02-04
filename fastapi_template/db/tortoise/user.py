from typing import List

from fastapi_template import shemas
from fastapi_template.db.models.users import Users

__all__ = ["UserRepository"]


class UserRepository:
    async def create(self, cmd: shemas.CreateUserCommand) -> shemas.User:
        u = Users(
            username=cmd.username,
            password=cmd.password.get_secret_value(),
            role_name=cmd.role_name,
        )
        await u.save()
        return shemas.User.from_orm(u)

    async def read(self, query: shemas.ReadUserByIdQuery) -> shemas.User:
        u = await Users.get(id=query.id)
        return shemas.User.from_orm(u)

    async def read_by_username(
        self,
        query: shemas.ReadUserByUserNameQuery,
    ) -> shemas.User:
        u = await Users.get(username=query.username)
        return shemas.User.from_orm(u)

    async def read_all(self) -> List[shemas.User]:
        u = await Users.all()
        result = [shemas.User.from_orm(item) for item in u]
        return result

    async def update(self, cmd: shemas.UpdateUserCommand) -> shemas.User:
        u = await Users.get(id=cmd.id)
        u.password = cmd.password.get_secret_value()
        await u.save()
        return shemas.User.from_orm(u)

    async def delete(self, cmd: shemas.DeleteUserCommand) -> shemas.User:
        u = await Users.get(id=cmd.id)
        result = shemas.User.from_orm(u)
        await u.delete()
        return result
