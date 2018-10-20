from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *

user_type_choices = ['Преподаватель', 'Администратор']
user_academic_status_choices = ['Ассистент', 'Старший преподаватель', 'Доцент', 'Профессор']


class User(Document):
    last_name = StringField(**default_string_params)
    first_name = StringField(**default_string_params)
    patronymic = StringField(**default_string_params)
    type = StringField(**default_string_params, choices=user_type_choices)
    birth_date = DateTimeField(**default_params)
    github_id = IntField(**default_params)
    stepic_id = IntField(**default_params)
    election_date = DateTimeField(**default_params)
    contract_date = DateTimeField(**default_params)
    academic_status = StringField(**default_string_params, choices=user_academic_status_choices)
    year_of_academic_status = DateTimeField(**default_params)
    meta = {'collection': 'Users'}