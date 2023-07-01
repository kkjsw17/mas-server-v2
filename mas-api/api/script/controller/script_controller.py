import inject
from fastapi import APIRouter

from api.auth.service.google_oauth2_service import GoogleOAuth2Service
from api.script.entity.script import Script
from api.script.service.script_service import ScriptService

router = APIRouter(tags=["User"])
google_oauth2_service = inject.instance(GoogleOAuth2Service)
script_service = inject.instance(ScriptService)


@router.get("/script/{meeting_id}")
async def get_current_user(meeting_id: int) -> list[Script]:
    """
    TODO
    """

    return await script_service.find_scripts_by_mid(meeting_id)
