from api.meeting.dto.meeting_dto import MeetingDto
from api.meeting.entity.meeting import Meeting
from api.meeting.repository.meeting_repository import MeetingRepository
from api.meeting.service.meeting_code_generation_service import (
    MeetingCodeGenerationService,
)


class MeetingService:
    """
    Service for handling operations related to Meeting entities.

    Attributes:
        meeting_repository (MeetingRepository): Repository for database operations related to Meeting.
        meeting_code_generation_service (MeetingCodeGenerationService): Service to generate meeting code.
    """

    def __init__(
        self,
        meeting_repository: MeetingRepository,
        meeting_code_generation_service: MeetingCodeGenerationService,
    ):
        self.meeting_repository = meeting_repository
        self.meeting_code_generation_service = meeting_code_generation_service

    async def create(self, meeting_dto: MeetingDto) -> Meeting:
        """
        Create a new Meeting with provided data and save it in the database.

        Args:
            meeting_dto (MeetingDto): Data transfer object containing meeting data.

        Returns:
            Meeting: Saved Meeting entity.
        """

        code = self.meeting_code_generation_service.get_meeting_code()
        meeting = Meeting(code=code, ongoing=True, **meeting_dto.model_dump())

        return await self.meeting_repository.save(meeting)

    async def find_ongoing_meeting_by_code(self, code: str) -> Meeting | None:
        """
        Find an ongoing Meeting by its code.

        Args:
            code (str): The code of the Meeting to find.

        Returns:
            Meeting | None: Meeting entity if found, otherwise None.
        """

        return await self.meeting_repository.find_meeting_by_code_and_ongoing(
            code=code, ongoing=True
        )
