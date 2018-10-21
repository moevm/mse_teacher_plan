from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)

from app import routes
