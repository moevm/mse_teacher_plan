from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.plans.default_model import default_params, default_string_params

user_type_choices = ['Преподаватель', 'Администратор', 'Менеджер']
user_academic_status_choices = ['Ассистент', 'Старший преподаватель', 'Доцент', 'Профессор']


class Profile(Document):
    user = ReferenceField('User')
    last_name = StringField(**default_string_params, verbose_name='Фамилия')
    first_name = StringField(**default_string_params, verbose_name='Имя')
    patronymic = StringField(**default_string_params, verbose_name='Отчество')
    type = StringField(**default_string_params, choices=user_type_choices, verbose_name='Тип', fixed=True)
    birth_date = DateTimeField(**default_params, verbose_name='Дата рождения', validate_rule='date')
    github_id = StringField(**default_string_params, verbose_name='Github ID', unique=True, validate_rule='id')
    stepic_id = StringField(**default_string_params, verbose_name='Stepic ID', unique=True, validate_rule='id')
    election_date = DateTimeField(**default_params, verbose_name='Дата избрания/зачисления')
    contract_date = DateTimeField(**default_params, verbose_name='Дата заключения конктракта')
    academic_status = StringField(**default_string_params, choices=user_academic_status_choices,
                                  verbose_name='Учебное звание')
    year_of_academic_status = IntField(**default_params, verbose_name='Год присуждения', validate_rule='year')
    meta = {'collection': 'Profiles'}
