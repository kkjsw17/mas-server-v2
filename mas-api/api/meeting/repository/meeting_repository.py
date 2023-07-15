from sqlalchemy import select

from api.common.database.database_connection_manager import DatabaseConnectionManager
from api.meeting.entity.meeting import Meeting


class MeetingRepository:
    def __init__(self, database: DatabaseConnectionManager):
        self.database = database

    async def save(self, meeting: Meeting) -> Meeting:
        async with self.database.get_session() as session:
            session.add(meeting)

        return meeting

    async def find_meetings_by_code_and_ongoing(
        self, code: str, ongoing: bool
    ) -> list[Meeting]:
        async with self.database.get_session() as session:
            result = await session.execute(
                select(Meeting).where(Meeting.code == code, Meeting.ongoing == ongoing)
            )
            meetings = result.scalars().all()

        return meetings
