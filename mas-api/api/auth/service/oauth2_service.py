import os
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from jose import jwt
from mas.api.auth.exception.auth_exception import OAuth2EncryptionKeyNotFoundException
from mas.api.user.entity.user import User
from mas.api.user.repository.user_repository import UserRepository
from mas.utils.config import Config
from mas.utils.const import (
    COOKIE_AUTHORIZATION_NAME,
    JWT_DECODING_OPTIONS,
    OAUTH2_ALGORITHM,
)
from mas.utils.datetime_utils import get_now_datetime_by_timezone
from mas.utils.oauth2_utils import OAuth2PasswordBearerWithCookie

oauth_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/token", authorization_name=COOKIE_AUTHORIZATION_NAME
)


class OAuth2Service(ABC):
    """
    Base class for an OAuth2 Service.

    Args:
        config (Config): A config instance containing settings for the OAuth2 service.
        user_repository (UserRepository): An instance of a user repository.
    """

    def __init__(self, config: Config, user_repository: UserRepository):
        self.config = config
        self.user_repository = user_repository

    @staticmethod
    @abstractmethod
    def get_account_info(access_token: str):
        raise NotImplementedError

    @abstractmethod
    def generate_token(self, access_token: str) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def refresh_token(self):
        raise NotImplementedError

    @abstractmethod
    def get_authorization_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_user_object_by_oauth2_info(self, id_info: dict[str, str | int]) -> User:
        raise NotImplementedError

    @staticmethod
    def create_access_token(
        data: dict, secret_key: str, algorithm: str = "HS256", expires_minutes: int = 30
    ) -> str:
        """
        Create a JWT token with the given data.

        Args:
            data (dict): The data to include in the token.
            secret_key (str): The secret key used to sign the token.
            algorithm (str, optional): The signing algorithm to use. Defaults to "HS256".
            expires_minutes (int, optional): The number of minutes until the token expires. Defaults to 30.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()

        expire = get_now_datetime_by_timezone() + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

        return encoded_jwt

    async def authenticate_user(self, email: str) -> User:
        """
        Authenticate a user with the given email.

        Args:
            email (str): The email of the user to authenticate.

        Returns:
            User: The authenticated user, or None if the user does not exist.
        """
        user = await self.user_repository.find_user_by_email(email)

        return user

    async def get_current_user(
        self, token: Annotated[str, Depends(oauth_scheme)]
    ) -> User:
        """
        Get the current authenticated user from the given JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            User: The authenticated user, or a new user created from the JWT token data if the user does not exist.
        """
        oauth2_encryption_key = os.getenv("OAUTH2_ENCRYPTION_KEY")
        if oauth2_encryption_key is None:
            raise OAuth2EncryptionKeyNotFoundException

        id_info = jwt.decode(
            token, oauth2_encryption_key, OAUTH2_ALGORITHM, options=JWT_DECODING_OPTIONS
        )
        email: str = id_info["email"]

        user = await self.authenticate_user(email)

        if user is None:
            user = self.create_user_object_by_oauth2_info(id_info)
            await self.user_repository.save(user)

        return user
