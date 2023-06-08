from datetime import datetime

from pydantic import BaseModel


class ScriptDto(BaseModel):
    name: str
    content: str
    created_at: datetime
