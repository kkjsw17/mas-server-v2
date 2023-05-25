from pydantic import BaseModel


class AuthTokenDTO(BaseModel):
    access_token: str
    token_type: str
