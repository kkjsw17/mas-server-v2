from typing import Annotated

import inject
from fastapi import APIRouter, Depends

from api.auth.service.google_oauth2_service import GoogleOAuth2Service
from api.user.dto.user_dto import UserDto
from api.user.entity.user import User
from api.user.service.user_service import UserService

router = APIRouter(tags=["User"])
google_oauth2_service = inject.instance(GoogleOAuth2Service)
user_service = inject.instance(UserService)


@router.get("/user/me")
async def get_current_user(
    user: Annotated[User, Depends(google_oauth2_service.get_current_user)]
) -> User:
    """
    Test endpoint that requires an authorized user. Returns the user object
    decoded from the encoded JWT token in the authorization cookie.

    Args:
        user (User): An annotated user object.

    Returns:
        User: The decoded user object.
    """

    return user


@router.get("/user")
async def get_all_user() -> list[User]:
    """ """
    users = await user_service.find_all()

    return users


@router.post("/user")
async def register_user(user_dto: UserDto) -> User:
    user = await user_service.register(**user_dto.dict())

    return user


@router.delete("/user/{user_id}")
async def get_entire_users(user_id: int) -> str:
    await user_service.delete(user_id)

    return "User deleted successfully"
