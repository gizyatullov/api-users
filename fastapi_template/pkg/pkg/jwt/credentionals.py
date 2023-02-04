from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from fastapi_template import shemas

__all__ = [
    "JwtService",
]


class JwtService:
    def __init__(
        self,
        access_security: JwtAccessBearer,
        refresh_security: JwtRefreshBearer,
    ):
        self.access_security = access_security
        self.refresh_security = refresh_security

    def get_access_token(self, user: shemas.User) -> str:
        return self.access_security.create_access_token(
            subject={"role_name": user.role_name},
            unique_identifier=user.username,
        )

    def get_refresh_token(self, user: shemas.User) -> str:
        return self.access_security.create_refresh_token(
            subject={"role_name": user.role_name},
            unique_identifier=user.username,
        )

    def get_token_pair(self, user: shemas.User) -> shemas.Auth:
        auth = shemas.Auth(
            access_token=self.get_access_token(user=user),
            refresh_token=self.get_refresh_token(user=user),
        )
        return auth
