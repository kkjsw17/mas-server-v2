import os

from api.api_initializer import APIInitializer
from api.utils.controller_utils import create_app
from api.utils.gunicorn_utils import MASMultiProcessingServer

APIInitializer(os.getenv("PHASE", "local"))

app = create_app("./api/api")

MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
