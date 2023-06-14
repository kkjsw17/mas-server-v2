from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from api.database.database_connection_manager import Base
from api.utils.datetime_utils import get_now_datetime_by_timezone


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
