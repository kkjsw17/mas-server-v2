import os

from api.api_initializer import APIInitializer
from api.common.middleware.logging_middleware import LoggingMiddleware
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer

APIInitializer(os.getenv("PHASE", "local"))

app = create_app(".")

# add middlewares
app.add_middleware(LoggingMiddleware, middleware_ignore_paths=[])

MASMultiProcessingServer(app, "./config/gunicorn.conf.toml").run()
