from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)
login = LoginManager(app)
login.login_view = 'login'

# noinspection PyUnresolvedReferences
from app import routes
