from mongoengine import StringField, DateTimeField

from app.models.default_model import *

reiteration_choices = ['Одноразовый', 'Повторяющийся']
publication_type_choices = ['Методическое указание', 'Книга', 'Статья в журнале', 'Сборник']


class Publication(DefaultModel):
    publication_type = StringField(**default_string_params, choices=publication_type_choices,
                                   verbose_name='Тип')
    reiteration = StringField(**default_string_params, choices=reiteration_choices, verbose_name='Вид повторения')
    name = StringField(**default_string_params, verbose_name='Название')
    unit_volume = StringField(**default_string_params, verbose_name='Единицы объема')
    publish_organization = StringField(**default_string_params, verbose_name='Название издательства')
    number = IntField(**default_params, verbose_name='Номер издания')
    volume = StringField(**default_string_params, verbose_name='Объем')
    edition = StringField(**default_string_params, verbose_name='Тираж')
    place = StringField(**default_string_params, verbose_name='Место издания')
    editor = StringField(**default_string_params, verbose_name='Редактор')
    date = DateTimeField(**default_params, verbose_name='Дата')
    ISBN = StringField(**default_string_params, verbose_name='ISBN')
    type = StringField(**default_string_params, verbose_name='Вид')
    meta = {'collection': 'Publications'}