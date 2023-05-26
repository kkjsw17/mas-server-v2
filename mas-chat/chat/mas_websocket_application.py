from mas.utils.controller_utils import create_app
from mas.utils.gunicorn_utils import MASMultiProcessingServer

app = create_app("./api/websocket", False)

MASMultiProcessingServer(app, "./config/websocket/gunicorn.conf.toml").run()
