from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField

from app.models.model import Model
from app.models.user import User

default_params = {'required': True}
default_string_params = {**default_params, 'max_length': 250}


class DefaultModel(Document):
    user = ReferenceField(User)
    model = ReferenceField(Model)
    year = IntField(**default_params)
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }
