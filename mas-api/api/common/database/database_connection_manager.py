import os
from abc import ABC, abstractmethod

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from api.utils.config import Config
from api.utils.const import DATABASE_DRIVER_CLASS
from api.utils.secret_utils import get_decrypted_password


class Base(MappedAsDataclass, DeclarativeBase):
    def dict(self):
        base_dict = self.__dict__
        base_dict.pop("_sa_instance_state")
        return base_dict


class DatabaseConnectionManager(ABC):
    """
    A base class for managing database connections.

    Args:
        config (Config): An instance of the Config class containing the configuration parameters.
        dbms_name (str): The name of the DBMS to connect to.
    """

    def __init__(self, config: Config, dbms_name: str):
        self.database_config = config.database[dbms_name]
        self.driver_class = DATABASE_DRIVER_CLASS["mysql"]
        self.endpoint = self.database_config["endpoint"]
        self.username = self.database_config["username"]
        self.password = get_decrypted_password(
            self.database_config["password"], os.getenv("DATABASE_ENCRYPTION_KEY")
        )
        self.port = self.database_config["port"]
        self.database_name = self.database_config["database_name"]

        self.database_url = f"{self.driver_class}://{self.username}:{self.password}@{self.endpoint}:{self.port}/{self.database_name}"
        print(self.database_url)

    @abstractmethod
    def connect_db(self):
        """
        Connects to the database.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect_db(self):
        """
        Disconnects from the database.
        """
        raise NotImplementedError

    @abstractmethod
    def get_session(self):
        """
        Returns a session object to interact with the database.
        """
        raise NotImplementedError
