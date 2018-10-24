from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *


class Other(Document):
    start_date = DateTimeField(**default_params, verbose_name='Дата начала')
    finish_date = DateTimeField(**default_params, verbose_name='Дата окончания')
    kind_of_work = StringField(**default_string_params, verbose_name='Вид работы')
    meta = {'collection': 'Other'}