from mongoengine import StringField
from app.models.plans.default_model import *


class Book(DefaultModel):
    authors = StringField(**default_string_params, verbose_name='Авторы')
    bookName = StringField(**default_string_params, verbose_name='Название')
    discipline = StringField(**default_string_params, verbose_name='Дисциплина')
    yeardate = IntField(**default_params, verbose_name='Год выпуска', validate_rule='allyear')
    organization = StringField(**default_string_params, verbose_name='Издательство')
    cipher = StringField(**default_string_params, verbose_name='Шифр')
    meta = {'collection': 'Books'}
