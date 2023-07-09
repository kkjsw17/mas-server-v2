from typing import Any

from fastapi import HTTPException, status


class ScriptValidationException(HTTPException):
    def __init__(
        self,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail: Any | None = "script_ids must be list of integer, like `1,2,3`",
        headers: dict[str, Any] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
