import os
from typing import Callable

from api.api_initializer import APIInitializer
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer
from fastapi import Request

APIInitializer(os.getenv("PHASE", "local"))

app = create_app("./api/api")


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    return response


MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
