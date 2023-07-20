from pydantic import BaseModel, field_validator


class MeetingDto(BaseModel):
    host_id: int
    title: str
    capacity: int

    @field_validator("title")
    @classmethod
    def check_title_length(cls, v: str) -> str:
        if len(v) > 20:
            raise ValueError("Title must be no longer than 20 characters long.")

        return v

    @field_validator("capacity")
    @classmethod
    def check_capacity(cls, v: int) -> int:
        if v < 0 or v > 10:
            raise ValueError(
                "Capacity must be no more than 10 people. We are trying to increase the number of meetings. 🥲"
            )

        return v
