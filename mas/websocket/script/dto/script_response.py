from datetime import datetime

from pydantic import BaseModel


class ScriptResponse(BaseModel):
    name: str
    content: str
    created_at: datetime
