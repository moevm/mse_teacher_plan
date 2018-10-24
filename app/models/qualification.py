from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *


class Qualification(Document):
    user = ReferenceField('User')
    course_name = StringField(**default_string_params, verbose_name='Название')
    discipline = StringField(**default_string_params, verbose_name='Дисциплина')
    authors = StringField(**default_string_params, verbose_name='Спикеры')
    start_date = DateTimeField(**default_params, verbose_name='Дата начала')
    finish_date = DateTimeField(**default_params, verbose_name='Дата окончания')
    organization = StringField(**default_string_params, verbose_name='Организация')
    meta = {'collection': 'Qualifications'}