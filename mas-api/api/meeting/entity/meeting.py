from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from api.common.database.database_connection_manager import Base
from api.utils.datetime_utils import get_now_datetime_by_timezone


class Meeting(Base):
    __tablename__ = "Meeting"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    host_id: Mapped[int]
    title: Mapped[str]
    code: Mapped[str]
    capacity: Mapped[int]
    ongoing: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
