from fastapi_template import shemas
from fastapi_template.pkg.pkg.exceptions.auth import IncorrectUsernameOrPassword
from fastapi_template.services.user import UserService


class AuthService:
    user_service: UserService

    def __init__(
        self,
        user_service: UserService,
    ):
        self.user_service = user_service

    async def check_user_password(self, cmd: shemas.AuthCommand) -> shemas.User:
        user = await self.user_service.read_specific_user_by_username(
            query=shemas.ReadUserByUserNameQuery(username=cmd.username),
            orm_obj=True
        )
        if not user or not await user.check_password(password=cmd.password):
            raise IncorrectUsernameOrPassword

        return shemas.User.from_orm(obj=user)
