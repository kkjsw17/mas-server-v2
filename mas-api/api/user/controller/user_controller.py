import inject
from fastapi import APIRouter

from api.user.service.user_service import UserService

router = APIRouter(tags=["User"])
user_service = inject.instance(UserService)


@router.get("/user/{user_id}")
async def get_user(user_id: int):
    return await user_service.find_user_by_id(user_id=user_id)
