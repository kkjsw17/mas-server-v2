from abc import ABC, abstractmethod


class OAuth2Service(ABC):
    @staticmethod
    @abstractmethod
    def get_account_info(access_token: str):
        raise NotImplementedError

    @abstractmethod
    def generate_token(self, access_token: str, token_type: str) -> dict[str, str]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def refresh_token():
        raise NotImplementedError
