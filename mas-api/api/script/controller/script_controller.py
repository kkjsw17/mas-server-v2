import re

import inject
from fastapi import APIRouter

from api.auth.service.google_oauth2_service import GoogleOAuth2Service
from api.script.entity.script import Script
from api.script.exception.script_validation_exception import ScriptValidationException
from api.script.service.script_service import ScriptService

router = APIRouter(tags=["Script"])
google_oauth2_service = inject.instance(GoogleOAuth2Service)
script_service = inject.instance(ScriptService)


@router.get("/script/{meeting_id}")
async def get_scripts(meeting_id: int) -> list[Script]:
    """
    Retrieve a list of scripts for a given meeting ID.

    Args:
        meeting_id (int): The ID of the meeting.

    Returns:
        list[Script]: A list of scripts matching the meeting ID.
    """

    return await script_service.find_scripts_by_mid(meeting_id)


@router.delete("/script/{script_ids}")
async def delete_scripts(script_ids: str) -> list[Script]:
    """
    Delete scripts with the specified script IDs.

    Args:
        script_ids (str): Comma-separated string of script IDs.

    Returns:
        list[Script]: A list of deleted scripts.
    """

    if not bool(re.match(r"^(\d+,)*\d+$", script_ids)):
        raise ScriptValidationException()

    script_ids = list(map(int, script_ids.split(",")))
    return await script_service.delete(script_ids)
