import inject

from mas.database.database_connection import DatabaseConnection
from mas.database.mysql_connection import MySQLConnection
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
        database_connection = MySQLConnection(self.config)
        binder.bind(DatabaseConnection, database_connection)
