from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from mas.database.database_connection_manager import Base
from mas.utils.datetime_utils import get_now_datetime_by_timezone


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    profile_image_url: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
