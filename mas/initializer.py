import inject

from mas.database.database_connection_manager import DatabaseConnectionManager
from mas.database.mysql_connection_manager import MySQLConnectionManager
from mas.user.repository.user_repository import UserRepository
from mas.utils.config import Config


class Initializer:
    """
    This class is responsible for initializing the application with necessary dependencies.

    Args:
        phase (str): The current phase of the application (e.g. development, production)
    """

    def __init__(self, phase: str):
        self.phase = phase
        self.config = Config(phase)
        inject.configure(self._bind)

    def _bind(self, binder: inject.Binder):
        """
        Binds the necessary dependencies for the application.

        Args:
            binder (inject.Binder): The binder object to bind the dependencies.
        """

        # 1. bind config
        binder.bind(Config, self.config)

        # 2. bind database connection
        database_connection = MySQLConnectionManager(self.config)
        database_connection.connect_db()
        binder.bind(DatabaseConnectionManager, database_connection)

        # 3. bind repositories
        user_repository = UserRepository(database=database_connection)
        binder.bind(UserRepository, user_repository)
