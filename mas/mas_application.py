from mas.utils.controller_utils import create_app
from mas.utils.gunicorn_utils import MASMultiThreadingServer

app = create_app()

MASMultiThreadingServer(app).run()
