from datetime import timedelta
from typing import Any, Mapping

from fastapi.security import OAuth2PasswordBearer
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from jwt import encode
from passlib.context import CryptContext

from mas.auth.service.oauth2_service import OAuth2Service
from mas.utils.datetime_utils import get_now_datetime_by_timezone


class GoogleOAuth2Service(OAuth2Service):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.auth_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def get_account_info(access_token: str) -> Mapping[str, Any]:
        account_info = verify_oauth2_token(access_token, requests.Request())

        return account_info

    def generate_token(self, access_token: str, token_type: str) -> dict[str, str]:
        account_info = self.get_account_info(access_token)
        email: str = account_info["hd"]

        now_datetime = get_now_datetime_by_timezone()

        token = {
            # TODO: 소멸 시간 상수로 빼기
            "exp": now_datetime + timedelta(minutes=30),
            "iat": now_datetime,
            "token_type": token_type,
            "email": email,
        }

        return {"access_token": encode(token)}

    @staticmethod
    def refresh_token():
        pass
