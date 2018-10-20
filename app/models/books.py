from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField
from app.models.default_params import *
from app.models.user import User


class Book(Document):
    user = ReferenceField(User)
    authors = StringField(**default_string_params)
    bookName = StringField(**default_string_params)
    discipline = StringField(**default_string_params)
    yeardate = IntField(**default_params)
    organization = StringField(**default_string_params)
    cipher = StringField(**default_string_params)