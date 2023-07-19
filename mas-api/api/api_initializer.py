import inject

from api.auth.service.google_oauth2_service import GoogleOAuth2Service
from api.common.database.database_connection_manager import DatabaseConnectionManager
from api.common.database.mysql_connection_manager import MySQLConnectionManager
from api.meeting.repository.meeting_repository import MeetingRepository
from api.meeting.service.meeting_code_generation_service import (
    MeetingCodeGenerationService,
)
from api.meeting.service.meeting_service import MeetingService
from api.script.repository.script_repository import ScriptRepository
from api.script.service.script_service import ScriptService
from api.user.repository.user_repository import UserRepository
from api.user.service.user_service import UserService
from api.utils.config import Config


class APIInitializer:
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

        print(config.oauth2)

        # 2. bind database connection
        database_connection = MySQLConnectionManager(config=config)
        binder.bind(DatabaseConnectionManager, database_connection)

        # 3. bind repositories
        user_repository = UserRepository(database=database_connection)
        binder.bind(UserRepository, user_repository)

        meeting_repository = MeetingRepository(database=database_connection)
        binder.bind(MeetingRepository, meeting_repository)

        script_repository = ScriptRepository(database=database_connection)
        binder.bind(ScriptRepository, script_repository)

        # 4. bind services
        user_service = UserService(user_repository=user_repository)
        binder.bind(UserService, user_service)

        google_oauth2_service = GoogleOAuth2Service(
            config=config, user_repository=user_repository
        )
        binder.bind(GoogleOAuth2Service, google_oauth2_service)

        meeting_service = MeetingService(meeting_repository=meeting_repository)
        binder.bind(MeetingService, meeting_service)

        meeting_code_generation_service = MeetingCodeGenerationService(
            meeting_repository=meeting_repository
        )
        binder.bind(MeetingCodeGenerationService, meeting_code_generation_service)

        script_service = ScriptService(script_repository=script_repository)
        binder.bind(ScriptService, script_service)
