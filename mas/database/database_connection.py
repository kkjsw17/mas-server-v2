import os
from abc import ABC, abstractmethod

from cryptography.fernet import Fernet

from mas.utils.config import Config
from mas.utils.const import DATABASE_DRIVER_CLASS


class DatabaseConnection(ABC):
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
        self.password = self.get_decrypted_password(
            self.database_config["password"], os.getenv("DATABASE_ENCRYPTION_KEY")
        )
        self.port = self.database_config["port"]
        self.database_name = self.database_config["database_name"]

        self.database_url = f"{self.driver_class}://{self.username}:{self.password}@{self.endpoint}:{self.port}/{self.database_name}"

    @abstractmethod
    async def connect_db(self):
        """
        Connects to the database.
        """
        raise NotImplementedError

    @abstractmethod
    async def disconnect_db(self):
        """
        Disconnects from the database.
        """
        raise NotImplementedError

    @staticmethod
    def get_decrypted_password(encrypted_password: str, key: str) -> str:
        """
        Decrypts a password using the provided key.

        Args:
            encrypted_password (str): The encrypted password to decrypt.
            key (str): The key used to decrypt the password.

        Returns:
            str: The decrypted password.
        """
        cipher_suite = Fernet(key)
        encoded_encrypted_password = encrypted_password.encode()

        return cipher_suite.decrypt(encoded_encrypted_password).decode()
