from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField
from app.models.default_params import *
from app.models.profile import Profile


class Discipline(Document):
    user = ReferenceField(Profile)
    disc = StringField(**default_string_params, verbose_name='Дисциплина')
    typeOfUpdate = StringField(**default_string_params, verbose_name='Характер изменений')
    type = StringField(**default_string_params, verbose_name='Тип')
    completeMark = StringField(**default_string_params, verbose_name='Отметка о выполнении')
    meta = {'collection': "Disciplines"}