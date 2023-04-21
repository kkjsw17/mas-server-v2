import inject

from mas.api.database.database_connection_manager import DatabaseConnectionManager
from mas.api.database.mysql_connection_manager import MySQLConnectionManager
from mas.api.script.repository.script_repository import ScriptRepository
from mas.utils.config import Config


class MessagingInitializer:
    """
    This class is responsible for initializing the application with necessary dependencies. TODO

    Args:
        phase (str): The current phase of the application (e.g. development, production)
    """

    def __init__(self, phase: str):
        self.phase = phase
        inject.configure(self._bind)

    def _bind(self, binder: inject.Binder):
        """
        Binds the necessary dependencies for the application.

        Args:
            binder (inject.Binder): The binder object to bind the dependencies.
        """

        # 1. bind config
        config = Config(self.phase)
        binder.bind(Config, config)

        # 2. bind database connection
        database_connection = MySQLConnectionManager(config=config)
        binder.bind(DatabaseConnectionManager, database_connection)

        # 3. bind repositories
        script_repository = ScriptRepository(database=database_connection)
        binder.bind(ScriptRepository, script_repository)
