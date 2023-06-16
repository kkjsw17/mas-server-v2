import os

from api.api_initializer import APIInitializer
from api.exception_handler.global_exception_handler import global_exception_handler
from api.middleware.logging_middleware import LoggingMiddleware
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer

APIInitializer(os.getenv("PHASE", "local"))

app = create_app(".")

# add middlewares
app.add_middleware(LoggingMiddleware, middleware_ignore_paths=[])

# add exception handlers
app.add_exception_handler(Exception, global_exception_handler)

MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
