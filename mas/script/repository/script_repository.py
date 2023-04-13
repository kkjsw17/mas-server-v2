from mas.database.database_connection_manager import DatabaseConnectionManager


class ScriptRepository:
    def __init__(self, database: DatabaseConnectionManager):
        self.database = database
