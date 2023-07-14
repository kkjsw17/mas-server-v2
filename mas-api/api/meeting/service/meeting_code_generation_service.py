import random
import string


class MeetingCodeGenerationService:
    def __init__(self, meeting_repository_service):
        self.meeting_repository_service = meeting_repository_service
        self.characters = string.ascii_letters + string.digits

    async def get_meeting_code(self):
        for code in iter(self._generate_random_code, None):
            if not await self._check_code_duplication_in_ongoing_meetings(code):
                return code

    def _generate_random_code(self, length: int | None = 6) -> str:
        return "".join(random.choices(self.characters, k=length))

    async def _check_code_duplication_in_ongoing_meetings(self, code: str) -> bool:
        meetings = await self.meeting_repository_service.find_by_code_and_ongoing(
            code=code, ongoing=True
        )

        return len(meetings) == 0
