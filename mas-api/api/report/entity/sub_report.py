from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from api.common.database.database_connection_manager import Base
from api.utils.datetime_utils import get_now_datetime_by_timezone


class SubReport(Base):
    __tablename__ = "SubReport"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    rid: Mapped[int]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=get_now_datetime_by_timezone
    )
