import os
from typing import Any

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from httpx_oauth.clients.google import GoogleOAuth2

from mas.auth.exception.auth_exception import OAuth2EncryptionKeyNotFoundException
from mas.auth.service.oauth2_service import OAuth2Service
from mas.user.entity.user import User
from mas.user.repository.user_repository import UserRepository
from mas.utils.config import Config
from mas.utils.const import OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES, OAUTH2_ALGORITHM
from mas.utils.secret_utils import get_decrypted_password


class GoogleOAuth2Service(OAuth2Service):
    """
    Class for the Google OAuth2 Service.

    Args:
        config (Config): A config instance containing settings for the OAuth2 service.
        user_repository (UserRepository): An instance of a user repository.

    Attributes:
        google_oauth_client (httpx_oauth.clients.google.GoogleOAuth2): The OAuth2 client for Google authentication.
    """

    def __init__(self, config: Config, user_repository: UserRepository):
        super().__init__(config=config, user_repository=user_repository)

        client_secret = get_decrypted_password(
            self.config.oauth2["google"]["client_secret"],
            os.getenv("OAUTH2_ENCRYPTION_KEY"),
        )

        self.google_oauth_client = GoogleOAuth2(
            client_id=config.oauth2["google"]["client_id"],
            client_secret=client_secret,
            scopes=config.oauth2["google"]["scopes"],
        )

    @staticmethod
    def get_account_info(access_token: str) -> dict[str, Any]:
        """
        Retrieves the account information from the access token.

        Args:
            access_token (str): The access token.

        Returns:
            dict[str, Any]: A dictionary containing the account information.
        """

        account_info = verify_oauth2_token(access_token, requests.Request())

        return account_info

    async def generate_token(self, code: str) -> str:
        """
        Generates an access token for the given authorization code.

        Args:
            code (str): The authorization code.

        Returns:
            A string containing the encoded JWT access token.
        """

        access_token = await self.google_oauth_client.get_access_token(
            code=code,
            redirect_uri=self.config.oauth2["google"]["redirect_uri"],
        )
        account_info = self.get_account_info(access_token["id_token"])

        oauth2_encryption_key = os.getenv("OAUTH2_ENCRYPTION_KEY")
        if oauth2_encryption_key is None:
            raise OAuth2EncryptionKeyNotFoundException

        encoded_jwt = self.create_access_token(
            account_info,
            oauth2_encryption_key,
            OAUTH2_ALGORITHM,
            OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return encoded_jwt

    def refresh_token(self):
        """
        TODO:
            - In the case of Google login, the refresh token is issued only once
            when the user logs into our web for the first time.
            - If the user logs in for the first time, a flow that stores the refresh token in the DB is required.
            - Since there is no web page for the registration flow yet, the refresh token is not considered yet.
        """

    async def get_authorization_url(self) -> str:
        """
        Generates an authorization URL to redirect the user for authentication.

        Returns:
            str: A string containing the authorization URL.

        TODO:
            These are the conditions that must be in order to obtain a refresh token issued.
            eg. &access_type=offline&prompt=consent
            The parameters will be changed to work only at the first login.
            https://hyeonic.github.io/woowacourse/dallog/google-refresh-token.html (Reference)
        """

        authorization_url = await self.google_oauth_client.get_authorization_url(
            redirect_uri=self.config.oauth2["google"]["redirect_uri"]
        )
        authorization_url += "&access_type=offline&prompt=consent"

        return authorization_url

    def create_user_object_by_oauth2_info(self, id_info: dict[str, str | int]) -> User:
        """
        Creates a new User object from the user data retrieved from Google OAuth2 authentication.

        Args:
            id_info (dict): A dictionary containing the user data.

        Returns:
            User: A new User object containing the user data.
        """

        new_user = User(
            email=id_info["email"],
            name=id_info["name"],
            given_name=id_info["given_name"],
            family_name=id_info["family_name"],
            locale=id_info["locale"],
            picture=id_info["picture"],
        )

        return new_user
