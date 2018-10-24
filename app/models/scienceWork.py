from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *
from app.models.profile import Profile


class ScienceWork(Document):
    user = ReferenceField(Profile)
    start_date = DateTimeField(**default_params, verbose_name='Дата начала')
    organization = StringField(**default_string_params, verbose_name='Организация')
    work_name = StringField(**default_string_params, verbose_name='Название научной работы')
    finish_date = DateTimeField(**default_params, verbose_name='Дата окончания')
    role = StringField(**default_string_params, verbose_name='Роль')
    cipher = StringField(**default_string_params, verbose_name='Шифр')
    meta = {'collection': 'ScienceWorks'}