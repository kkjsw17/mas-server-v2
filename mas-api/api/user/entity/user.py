from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from api.common.database.database_connection_manager import Base
from api.utils.datetime_utils import get_now_datetime_by_timezone


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column()
    name: Mapped[str]
    given_name: Mapped[str]
    family_name: Mapped[str]
    locale: Mapped[str]
    picture: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
