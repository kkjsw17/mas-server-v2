from datetime import datetime

from messaging.database.database_connection_manager import Base
from pytz import timezone
from sqlalchemy.orm import Mapped, mapped_column


def get_now_datetime_by_timezone(timezone_str: str = "Asia/Seoul") -> datetime:
    """
    Returns a datetime object with the specified timezone.

    Args:
        timezone_str (str): The target timezone, in Olson format (e.g. 'America/New_York').

    Returns:
        datetime: A datetime object with the specified timezone.
    """
    return datetime.now(timezone(timezone_str))


class Script(Base):
    __tablename__ = "Script"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    mid: Mapped[int]
    uid: Mapped[int]
    content: Mapped[str]
    checked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
