from logging import getLogger
from uuid import uuid4

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = getLogger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid4())

        logger.info(f"[{request_id}] | REQ | {request}")
        response = await call_next(request)
        logger.info(f"[{request_id}] | RSP | {response}")

        return response
