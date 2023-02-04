from typing import List

from fastapi import APIRouter, status

from fastapi_template import shemas
from fastapi_template.services import user_service

router = APIRouter()


@router.post(
    "/",
    response_model=shemas.User,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    response_model_exclude={"password"},
)
async def create_user(
    cmd: shemas.CreateUserCommand,
):
    return await user_service.create_user(cmd=cmd)


@router.get(
    "/",
    response_model=List[shemas.User],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Get all users without password field.",
)
async def read_all_users():
    return await user_service.read_all_users()


@router.get(
    "/{user_id:int}",
    response_model=shemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field.",
)
async def read_user(
    user_id: int = shemas.UserFields.id,
):
    return await user_service.read_specific_user_by_id(
        query=shemas.ReadUserByIdQuery(id=user_id),
    )


@router.get(
    "/{username:str}",
    response_model=shemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field.",
)
async def read_user(
    username: str = shemas.UserFields.username,
):
    return await user_service.read_specific_user_by_username(
        query=shemas.ReadUserByUserNameQuery(username=username),
    )


@router.patch(
    "/password",
    response_model=shemas.User,
    status_code=status.HTTP_202_ACCEPTED,
    description="Change password.",
    response_model_exclude={"password"},
)
async def change_password(
    cmd: shemas.ChangeUserPasswordCommand,
):
    return await user_service.change_password(cmd=cmd)


@router.delete(
    "/{user_id}",
    response_model=shemas.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Delete specific user",
)
async def delete_user(
    user_id: int = shemas.UserFields.id,
):
    return await user_service.delete_specific_user(
        cmd=shemas.DeleteUserCommand(id=user_id),
    )