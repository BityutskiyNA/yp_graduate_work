from gevent import monkey

monkey.patch_all(thread=True)

from gevent.pywsgi import WSGIServer
from src.settings import app_settings

from src.logger import logger

# from geventwebsocket.handler import WebSocketHandler
from main_app import create_app

app = create_app()

http_server = WSGIServer(("0.0.0.0", app_settings.port), app)
logger.info("Starting gevent WSGI Server")
http_server.serve_forever()
