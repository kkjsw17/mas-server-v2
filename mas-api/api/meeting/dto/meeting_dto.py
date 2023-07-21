from pydantic import BaseModel, field_validator

from api.utils.const import (
    MEETING_CAPACITY_VALIDATION_MESSAGE,
    MEETING_TITLE_LENGTH_VALIDATION_MESSAGE,
)


class MeetingDto(BaseModel):
    host_id: int
    title: str
    capacity: int

    @field_validator("title")
    @classmethod
    def check_title_length(cls, v: str) -> str:
        if len(v) > 20:
            raise ValueError(MEETING_TITLE_LENGTH_VALIDATION_MESSAGE)

        return v

    @field_validator("capacity")
    @classmethod
    def check_capacity(cls, v: int) -> int:
        if v < 0 or v > 10:
            raise ValueError(MEETING_CAPACITY_VALIDATION_MESSAGE)

        return v
