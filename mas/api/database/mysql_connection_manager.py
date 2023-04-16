from asyncio import current_task
from contextlib import AbstractContextManager, asynccontextmanager
from logging import getLogger
from typing import Callable

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from mas.api.database.database_connection_manager import DatabaseConnectionManager
from mas.utils.config import Config

logger = getLogger()


class MySQLConnectionManager(DatabaseConnectionManager):
    """
    A class for managing MySQL database connections.

    Args:
        config (Config): An instance of the Config class containing the configuration parameters.
        dbms_name (str): The name of the DBMS to connect to. (default mysql)
    """

    def __init__(self, config: Config, dbms_name: str = "mysql"):
        super().__init__(config, dbms_name)

        self._engine = None
        self._session_factory = None

    async def connect_db(self):
        """
        Connects to the MySQL database.
        """
        self._engine = create_async_engine(
            self.database_url,
            echo=True,
            future=True,
            poolclass=NullPool,
        )
        self._session_factory = async_scoped_session(
            session_factory=async_sessionmaker(
                bind=self._engine, class_=AsyncSession, expire_on_commit=False
            ),
            scopefunc=current_task,
        )

    async def disconnect_db(self):
        """
        Disconnects from the MySQL database.
        """
        await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        """
        Returns an async SQLAlchemy session object to interact with the database.

        Returns:
            AsyncSession: An async SQLAlchemy session object to interact with the database.
        """
        session: AsyncSession = self._session_factory()

        try:
            yield session
            await session.commit()
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
            await self._session_factory.remove()
