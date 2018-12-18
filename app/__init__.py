import logging.config

import sentry_sdk
from flask import Flask
from flask.logging import default_handler
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from config.config import Config

sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn="https://6fd2141e720544de9ec65b07ec202302@sentry.io/1337579",
    integrations=[FlaskIntegration(), sentry_logging]
)

# logging.config.fileConfig('config/logging.conf')  # Comment this while testing. TODO Fix logging in unit tests
logging.info(f'||Starting {__name__}||')
app = Flask(__name__)
app.config.from_object(Config)
app.logger.removeHandler(default_handler)
db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)
login = LoginManager(app)
login.login_view = 'login'
# noinspection PyUnresolvedReferences
from app.routing import routes

