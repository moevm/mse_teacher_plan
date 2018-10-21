from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *

user_type_choices = ['Преподаватель', 'Администратор']
user_academic_status_choices = ['Ассистент', 'Старший преподаватель', 'Доцент', 'Профессор']


class User(Document):
    last_name = StringField(**default_string_params, verbose_name='Фамилия')
    first_name = StringField(**default_string_params, verbose_name='Имя')
    patronymic = StringField(**default_string_params, verbose_name='Отчество')
    type = StringField(**default_string_params, choices=user_type_choices, verbose_name='Тип')
    birth_date = DateTimeField(**default_params, verbose_name='Дата рождения')
    github_id = IntField(**default_params, verbose_name='Github ID')
    stepic_id = IntField(**default_params, verbose_name='Stepic ID')
    election_date = DateTimeField(**default_params, verbose_name='Дата избрания/зачисления')
    contract_date = DateTimeField(**default_params, verbose_name='Дата заключения конктракта')
    academic_status = StringField(**default_string_params, choices=user_academic_status_choices,
                                  verbose_name='Учебное звание')
    year_of_academic_status = IntField(**default_params, verbose_name='Год присуждения')
    meta = {'collection': 'Users'}