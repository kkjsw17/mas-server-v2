from chat.utils.controller_utils import create_app
from chat.utils.gunicorn_utils import MasWebsocketChatServer

app = create_app(".")

MasWebsocketChatServer(app, "./config/gunicorn.conf.toml").run()
