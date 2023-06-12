import os
from logging import getLogger
from typing import Callable
from uuid import uuid4

from api.api_initializer import APIInitializer
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer
from fastapi import Request
from fastapi.responses import JSONResponse

APIInitializer(os.getenv("PHASE", "local"))

app = create_app("./api/api")
logger = getLogger()


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable):
    request_id = str(uuid4())
    logger.info(f"[{request_id}] | REQ | {request}")
    response = await call_next(request)
    logger.info(f"[{request_id}] | RSP | {response}")
    return response


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
