import os

from fastapi import Request
from fastapi.responses import JSONResponse

from api.api_initializer import APIInitializer
from api.middleware.logging_middleware import LoggingMiddleware
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer

APIInitializer(os.getenv("PHASE", "local"))

app = create_app(".")
app.add_middleware(LoggingMiddleware)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
