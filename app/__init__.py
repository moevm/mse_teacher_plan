import logging.config

import sentry_sdk
from flask import Flask
from flask.logging import default_handler
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.config.config import Config

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=Config.SENTRY_DSN,
    integrations=[FlaskIntegration(), sentry_logging]
)

logging.config.fileConfig('app/config/logging.conf')  # This stuff will probaly crash while unit testing.
logging.info(f'||Starting {__name__}||')  # To resolve this, set working directory to the project root
app = Flask(__name__)
app.config.from_object(Config)
app.logger.removeHandler(default_handler)
db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)
login = LoginManager(app)
login.login_view = 'login'
# noinspection PyUnresolvedReferences
from app.routing import routes

