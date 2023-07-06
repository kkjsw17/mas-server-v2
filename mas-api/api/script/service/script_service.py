from api.script.entity.script import Script
from api.script.repository.script_repository import ScriptRepository


class ScriptService:
    """
    Service class to handle business logics related to scripts

    Args:
        script_repository (ScriptRepository): script repository instance
    """

    def __init__(self, script_repository: ScriptRepository):
        self.script_repository = script_repository

    async def find_scripts_by_mid(self, meeting_id: int) -> list[Script]:
        """
        Retrieve a list of scripts by meeting ID.

        Args:
            meeting_id (int): Meeting ID.

        Returns:
            list[Script]: List of scripts associated with the meeting ID.
        """

        return await self.script_repository.find_scripts_by_mid(meeting_id)

    async def delete(self, script_ids: list[int]) -> list[Script]:
        """
        Delete scripts with the specified IDs.

        Args:
            script_ids (list[int]): List of script IDs to be deleted.

        Returns:
            list[Script]: List of scripts that deleted.
        """

        return await self.script_repository.delete(script_ids)
