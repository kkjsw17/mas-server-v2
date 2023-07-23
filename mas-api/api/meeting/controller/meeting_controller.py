import inject
from fastapi import APIRouter

from api.meeting.dto.meeting_dto import MeetingDto
from api.meeting.entity.meeting import Meeting
from api.meeting.service.meeting_service import MeetingService

router = APIRouter(tags=["Meeting"])
meeting_service = inject.instance(MeetingService)


@router.post("/meeting")
async def create_meeting(meeting_dto: MeetingDto) -> Meeting:
    return await meeting_service.create(meeting_dto=meeting_dto)
