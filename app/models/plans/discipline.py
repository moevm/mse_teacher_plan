from mongoengine import StringField
from app.models.plans.default_model import *


class Discipline(DefaultModel):
    disc = StringField(**default_string_params, verbose_name='Дисциплина')
    typeOfUpdate = StringField(**default_string_params, verbose_name='Характер изменений')
    type = StringField(**default_string_params, verbose_name='Тип')
    completeMark = StringField(**default_string_params, verbose_name='Отметка о выполнении')
    meta = {'collection': "Disciplines"}
