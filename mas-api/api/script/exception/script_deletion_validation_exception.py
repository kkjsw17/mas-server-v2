from typing import Any

from fastapi import HTTPException, status

from api.utils.const import SCRIPT_DELETION_VALIDATION_EXCEPTION_MESSAGE


class ScriptDeletionValidationException(HTTPException):
    def __init__(
        self,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail: Any | None = SCRIPT_DELETION_VALIDATION_EXCEPTION_MESSAGE,
        headers: dict[str, Any] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
