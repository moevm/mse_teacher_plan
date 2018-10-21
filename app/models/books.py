from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField
from app.models.default_params import *
from app.models.profile import Profile


class Book(Document):
    user = ReferenceField(Profile)
    authors = StringField(**default_string_params, verbose_name='Авторы')
    bookName = StringField(**default_string_params, verbose_name='Название')
    discipline = StringField(**default_string_params, verbose_name='Дисциплина')
    yeardate = IntField(**default_params, verbose_name='Год выпуска')
    organization = StringField(**default_string_params, verbose_name='Издательство')
    cipher = StringField(**default_string_params, verbose_name='Шифр')
    meta = {'collection': 'Books'}