from typing import List, Union
import datetime

from fastapi_template import shemas
from fastapi_template.db.models.users import Users
from fastapi_template.pkg.pkg.exceptions.user import IncorrectOldPassword

__all__ = ["UserRepository"]


class UserRepository:
    async def create(self, cmd: shemas.CreateUserCommand) -> shemas.User:
        u = Users(
            username=cmd.username,
            role_name=cmd.role_name,
        )
        await u.set_password(password=cmd.password)
        await u.save()
        return shemas.User.from_orm(u)

    async def read(self,
                   query: shemas.ReadUserByIdQuery,
                   orm_obj: bool = False) -> Union[shemas.User, Users]:
        u = await Users.get(id=query.id)
        if orm_obj:
            return u
        return shemas.User.from_orm(u)

    async def read_by_username(
        self,
        query: shemas.ReadUserByUserNameQuery,
        orm_obj: bool = False
    ) -> Union[shemas.User, Users]:
        u = await Users.get(username=query.username)
        if orm_obj:
            return u
        return shemas.User.from_orm(u)

    async def read_all(self) -> List[shemas.User]:
        u = await Users.all()
        result = [shemas.User.from_orm(item) for item in u]
        return result

    async def delete(self, cmd: shemas.DeleteUserCommand) -> shemas.User:
        u = await Users.get(id=cmd.id)
        result = shemas.User.from_orm(u)
        await u.delete()
        return result

    async def change_password(self,
                              cmd: shemas.ChangeUserPasswordCommand) -> shemas.User:
        u = await self.read(query=shemas.ReadUserByIdQuery(id=cmd.id), orm_obj=True)
        if not u or not await u.check_password(password=cmd.old_password):
            raise IncorrectOldPassword
        await u.set_password(password=cmd.new_password)
        await u.save()
        return shemas.User.from_orm(obj=u)

    async def update_specific_user_by_username(self,
                                               cmd: shemas.UpdateUserCommand) -> shemas.User:
        u = await self.read_by_username(
            query=shemas.ReadUserByUserNameQuery(username=cmd.username),
            orm_obj=True)

        for k, v in cmd.dict(exclude={'username'}, exclude_none=True).items():
            if k in ('user_ban_date',):
                v = datetime.datetime.fromisoformat(v)
            setattr(u, k, v)

        await u.save()

        return shemas.User.from_orm(obj=u)
