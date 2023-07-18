from api.meeting.entity.meeting import Meeting
from api.meeting.repository.meeting_repository import MeetingRepository


class MeetingService:
    def __init__(self, meeting_repository: MeetingRepository):
        self.meeting_repository = meeting_repository

    async def find_ongoing_meeting_by_code(self, code: str) -> Meeting | None:
        return await self.meeting_repository.find_meeting_by_code_and_ongoing(
            code=code, ongoing=True
        )
