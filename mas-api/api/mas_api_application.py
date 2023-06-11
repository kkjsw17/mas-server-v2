import os
from typing import Callable

from api.api_initializer import APIInitializer
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer
from fastapi import Request
from fastapi.responses import JSONResponse

APIInitializer(os.getenv("PHASE", "local"))

app = create_app("./api/api")


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
