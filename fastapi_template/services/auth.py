from fastapi_template import shemas
from fastapi_template.pkg.pkg.exceptions.auth import IncorrectUsernameOrPassword
from fastapi_template.pkg.pkg.password import password
from fastapi_template.services.user import UserService


class AuthService:
    # refresh_token_repository: JWTRefreshTokenRepository
    user_service: UserService

    def __init__(
        self,
        user_service: UserService,
        # refresh_token_repository: JWTRefreshTokenRepository,
    ):
        """
        Initialize class for auth methods.

        Args:
            user_service: User interface implementation.
            refresh_token_repository: Refresh token interface implementation.
        """
        self.user_service = user_service
        # self.refresh_token_repository = refresh_token_repository

    async def check_user_password(self, cmd: shemas.AuthCommand) -> shemas.User:
        user = await self.user_service.read_specific_user_by_username(
            query=shemas.ReadUserByUserNameQuery(username=cmd.username),
        )
        if user is None or not password.check_password(cmd.password, user.password):
            raise IncorrectUsernameOrPassword

        return user
