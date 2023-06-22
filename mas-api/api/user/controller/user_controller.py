from typing import Annotated

import inject
from fastapi import APIRouter, Depends

from api.auth.service.google_oauth2_service import GoogleOAuth2Service
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
