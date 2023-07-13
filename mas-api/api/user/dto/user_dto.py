from pydantic import BaseModel, EmailStr, HttpUrl

from api.user.enum.locale import Locale


class UserDto(BaseModel):
    email: EmailStr
    name: str
    given_name: str
    family_name: str
    locale: Locale
    picture: HttpUrl | None
