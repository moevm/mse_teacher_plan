from typing import Union

from bson import ObjectId
from mongoengine.document import Document
from mongoengine.fields import StringField


default_params = {'required': True}
default_string_params = {**default_params, 'max_length': 250}


class Model(Document):
    text = StringField(**default_params)
    name = StringField(**default_params)
    fileName = StringField(**default_params)
    className = StringField(**default_params)
    meta = {'collection': 'Models'}


DocId = Union[int, str, ObjectId]