from mas.database.database_connection_manager import DatabaseConnectionManager
from mas.script.entity.script import Script


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
