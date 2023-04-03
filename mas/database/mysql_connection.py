from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from mas.database.database_connection import DatabaseConnection
from mas.utils.config import Config


class MySQLConnection(DatabaseConnection):
    """
    A class for managing MySQL database connections.

    Args:
        config (Config): An instance of the Config class containing the configuration parameters.
        dbms_name (str): The name of the DBMS to connect to. (default mysql)
    """

    def __init__(self, config: Config, dbms_name: str = "mysql"):
        super().__init__(config, dbms_name)

        self.engine = None
        self.async_session = None

    async def get_session(self) -> async_sessionmaker[AsyncSession]:
        """
        Returns an async SQLAlchemy session object to interact with the database.

        Returns:
            AsyncSession: An async SQLAlchemy session object to interact with the database.
        """
        return self.async_session

    async def connect_db(self):
        """
        Connects to the MySQL database.
        """
        self.engine = create_async_engine(
            self.database_url,
            echo=True,
            future=True,
            poolclass=NullPool,
        )
        self.async_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def disconnect_db(self):
        """
        Disconnects from the MySQL database.
        """
        await self.engine.dispose()
