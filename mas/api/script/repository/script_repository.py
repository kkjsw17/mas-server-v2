from sqlalchemy import delete

from mas.api.database.database_connection_manager import DatabaseConnectionManager
from mas.api.script.entity.script import Script


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

    async def delete(self, script_id: int) -> Script | None:
        """
        Delete a script with the given script ID.

        Args:
            script_id (int): The ID of the script to delete.

        Returns:
            Script | None: Deleted user or None
        """
        async with self.database.get_session() as session:
            result = await session.execute(delete(Script).where(Script.id == script_id))

            deleted_script = result.scalars().one_or_none()

        return deleted_script
