import inject

from mas.auth.service.google_oauth2_service import GoogleOAuth2Service
from mas.database.database_connection_manager import DatabaseConnectionManager
from mas.database.mysql_connection_manager import MySQLConnectionManager
from mas.script.service.script_websocket_management_service import (
    ScriptWebsocketManagementService,
)
from mas.user.repository.user_repository import UserRepository
from mas.user.service.user_service import UserService
from mas.utils.config import Config


class Initializer:
    """
    This class is responsible for initializing the application with necessary dependencies.

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
        user_repository = UserRepository(database=database_connection)
        binder.bind(UserRepository, user_repository)

        # 4. bind services
        websocket_connection_management_service = ScriptWebsocketManagementService()
        binder.bind(
            ScriptWebsocketManagementService,
            websocket_connection_management_service,
        )

        user_service = UserService(user_repository=user_repository)
        binder.bind(UserService, user_service)

        google_oauth2_service = GoogleOAuth2Service(
            config=config, user_repository=user_repository
        )
        binder.bind(GoogleOAuth2Service, google_oauth2_service)
