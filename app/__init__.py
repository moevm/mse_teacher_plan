import logging

from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn="https://6fd2141e720544de9ec65b07ec202302@sentry.io/1337579",
    integrations=[FlaskIntegration(), sentry_logging]
)

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)
login = LoginManager(app)
login.login_view = 'login'

# noinspection PyUnresolvedReferences
from app import routes
