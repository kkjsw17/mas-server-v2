from dataclasses import dataclass, field
from datetime import datetime

from chat.utils.datetime_utils import get_now_datetime_by_timezone


@dataclass
class Script:
    mid: int
    uid: int
    content: str
    checked: bool = False
    created_at: datetime = field(default_factory=get_now_datetime_by_timezone)
    modified_at: datetime = field(default_factory=get_now_datetime_by_timezone)
