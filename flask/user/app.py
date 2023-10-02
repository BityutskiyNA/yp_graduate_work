import logstash
from flask import Flask, request
from src.databases.db import add_admin_and_roles
from src.models.user import User
from src.models.message_type import Message_type
from src.models.role import Role
from src.models import user_role
from src.models.session import Session
from src.models.token import Token
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from src.api.v1.admin.user import bp_admin_user
from src.api.v1.admin.role import bp_admin_role
from src.api.v1.auth import bp_auth
from src.api.v1.token import bp_token
from src.api.v1.notification import bp_notification
from config import config
import logging


import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn=config.flask.sentry_dsn,
    integrations=[
        FlaskIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.jaeger.agent_host_name,
                agent_port=config.jaeger.agent_port,
            )
        )
    )

    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


# init app
# configure_tracer()
app = Flask(__name__)
app.config["SECRET_KEY"] = config.flask.secret_key
# logging.basicConfig(level=logging.INFO)

# app.logger = logging.getLogger(__name__)
# app.logger.setLevel(logging.INFO)

# app.logger.addHandler(logstash.LogstashHandler("logstash", 5044, version=1))
# Handler отвечают за вывод и отправку сообщений.
# В модуль logging доступно несколько классов-обработчиков
# Например, SteamHandler для записи в поток stdin/stdout, DatagramHandler для UDP, FileHandler для syslog
# LogstashHandler не только отправляет данные по TCP/UDP, но и форматирует логи в json-формат.


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


app.logger.addFilter(RequestIdFilter())

FlaskInstrumentor().instrument_app(app)


# @app.before_request
# def before_request():
#     request_id = request.headers.get("X-Request-Id")
#     if not request_id:
#         raise RuntimeError("request id is required")


# models
models = {
    "user": User,
    "role": Role,
    "message_type": Message_type,
    "user_role": user_role,
    "session": Session,
    "token": Token,
}

# add roles and admin
add_admin_and_roles(app, User, Role)

# add routers
app.register_blueprint(bp_admin_user)
app.register_blueprint(bp_admin_role)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_token)
app.register_blueprint(bp_notification)

app.run(debug=True)
