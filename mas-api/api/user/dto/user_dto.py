# from datetime import datetime
#
# from sqlalchemy.orm import Mapped, mapped_column
#
# from api.common.database.database_connection_manager import Base
# from api.utils.datetime_utils import get_now_datetime_by_timezone

from pydantic import BaseModel, EmailStr, HttpUrl


class UserDto(BaseModel):
    email: EmailStr
    name: str
    given_name: str
    family_name: str
    locale: str
    picture: HttpUrl | None
