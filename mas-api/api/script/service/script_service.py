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
        """"""
        return await self.script_repository.find_scripts_by_mid(meeting_id)

    async def delete(self, script_id: int):
        """ """
        await self.script_repository.delete(script_id)
