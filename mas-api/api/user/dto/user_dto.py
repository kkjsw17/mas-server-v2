from pydantic import BaseModel, EmailStr, HttpUrl


class UserDto(BaseModel):
    email: EmailStr
    name: str
    given_name: str
    family_name: str
    locale: str
    picture: HttpUrl | None
