from mongoengine import DateTimeField, StringField
from app.models.default_model import *


class ScienceWork(DefaultModel):
    start_date = DateTimeField(**default_params, verbose_name='Дата начала')
    organization = StringField(**default_string_params, verbose_name='Организация')
    work_name = StringField(**default_string_params, verbose_name='Название научной работы')
    finish_date = DateTimeField(**default_params, verbose_name='Дата окончания')
    role = StringField(**default_string_params, verbose_name='Роль')
    cipher = StringField(**default_string_params, verbose_name='Шифр')
    meta = {'collection': 'ScienceWorks'}