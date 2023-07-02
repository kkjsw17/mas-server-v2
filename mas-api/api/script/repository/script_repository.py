from sqlalchemy import delete, select

from api.common.database.database_connection_manager import DatabaseConnectionManager
from api.script.entity.script import Script


class ScriptRepository:
    def __init__(self, database: DatabaseConnectionManager):
        self.database = database

    async def save(self, script: Script) -> Script:
        """
        Save the given script object to the database.

        Args:
            script (Script): The Script object to save to the database.

        Returns:
            Script: The saved User object.
        """
        async with self.database.get_session() as session:
            session.add(script)

        return script

    async def find_scripts_by_mid(self, meeting_id: int) -> list[Script]:
        async with self.database.get_session() as session:
            result = await session.execute(
                select(Script).where(Script.mid == meeting_id)
            )
            scripts = result.scalars().all()

        return scripts

    async def delete(self, script_ids: list[int]) -> Script | None:
        """
        Delete scripts with the given script IDs.

        Args:
            script_ids (int): The ID of the script to delete.

        Returns:
            Script | None: Deleted user or None
        """
        async with self.database.get_session() as session:
            result = await session.execute(
                delete(Script).where(Script.id.in_(script_ids))
            )

            deleted_script = result.scalars().all()

        return deleted_script
