from mongoengine import DateTimeField, StringField
from models.plans.default_model import *


class Other(DefaultModel):
    start_date = DateTimeField(**default_params, verbose_name='Дата начала')
    finish_date = DateTimeField(**default_params, verbose_name='Дата окончания')
    kind_of_work = StringField(**default_string_params, verbose_name='Вид работы')
    meta = {'collection': 'Other'}