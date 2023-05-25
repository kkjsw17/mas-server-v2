import os

from mas.api.api_initializer import APIInitializer
from mas.utils.controller_utils import create_app
from mas.utils.gunicorn_utils import MASMultiProcessingServer

APIInitializer(os.getenv("PHASE", "local"))

app = create_app("./api/api")

MASMultiProcessingServer(app, "./config/api/gunicorn.conf.toml").run()
