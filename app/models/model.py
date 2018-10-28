from mongoengine.document import Document
from mongoengine.fields import StringField
from app.models.default_model import default_params


class Model(Document):
    text = StringField(**default_params)
    name = StringField(**default_params)
    fileName = StringField(**default_params)
    className = StringField(**default_params)
    meta = {'collection': 'Models'}