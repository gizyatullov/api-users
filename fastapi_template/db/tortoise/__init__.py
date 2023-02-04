from dependency_injector import containers, providers

from .user import UserRepository


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Factory(UserRepository)
