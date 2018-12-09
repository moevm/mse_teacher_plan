from mongoengine.document import Document
from mongoengine.fields import StringField

from models.plans.default_model import default_string_params


class Report(Document):
    name = StringField(**default_string_params)
    text = StringField(**default_string_params)
    min_auth = StringField(**default_string_params)
    meta = {
        'collection': 'Reports'
    }
