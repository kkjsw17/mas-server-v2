import json
from logging import getLogger
from uuid import uuid4

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from api.common.middleware.middleware_utils import AsyncIteratorWrapper, set_body

logger = getLogger()


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, middleware_ignore_paths: list[str]) -> None:
        super().__init__(app)

        self.middleware_ignore_paths = middleware_ignore_paths

    @staticmethod
    async def _log_request(request: Request):
        headers = dict(zip(request.headers.keys(), request.headers.values()))
        body = await request.json()

        log_message = f"[{request.url.path} / {request.state.request_id}] | REQ | HEADERS: {headers} | BODY: {body}"

        if request.query_params:
            log_message += f" | QUERY_PARAMS: {request.query_params}"

        logger.info(log_message)

        return body

    @staticmethod
    async def _log_response(request: Request, response: Response):
        headers = dict(response.headers)
        body = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", AsyncIteratorWrapper(body))

        try:
            body = json.loads(body[0].decode())
        except Exception:
            body = str(body)

        log_message = f"[{request.url.path} / {request.state.request_id}] | RSP | HEADERS: {headers} | BODY: {body}"
        logger.info(log_message)

        return body

    async def _middleware_logic(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        await set_body(request)

        await self._log_request(request)
        response = await call_next(request)
        await self._log_response(request, response)

        return response

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.request_id = str(uuid4())

        if request.url.path in self.middleware_ignore_paths:
            response = await call_next(request)
        else:
            response = await self._middleware_logic(request, call_next)

        return response
