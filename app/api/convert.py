"""
===================================
API Для конвертации моделей MongoDB
===================================
Информацию о моделях БД нужно передавать в JavaScript и т.п. Функции этого файла переводят
модели mongoDB в более удобные для работы объекты и обратно.
Структура конвертированной модели -
    [
        {
            'text'  - отображаемый текст. Может быть %NO_VERBOSE_NAME%
            'name'  - короткое обозначение
            'type'  - тип. Может быть Date, Number или String
            'opts'  - список принимаемых значений. Если пустой, то значения любые
            'value' - значение. Пустое для модели и заполненное для документа.
            'fixed' - разрешено ли изменять
            'validate_rule' - правило валидации
        }
    ]
Генератор форм (inputForm.html) позволяет осуществлять валидацию. Типы валидации следующие:
    'text' - [0-9. A-Za-zА-Яа-яЁё]{1,1000}
    'token' - [0-9a-f]{1,30}
    'string' - [0-9-A-Za-zА-Яа-яЁё_.]{1,50}
    'id' - [0-9A-Za-z_.]{1,50}
    'date' - Дата от 01/01/1990 до текущего
    'alldate' - Дата от 01/01/1990 до 01/01/2100
    'year' - от 1900 до текущего
    'allyear' - от 1900 до 2100
Валидация по умолчанию:
    Текст - 'text'
    Дата - 'alldate'
    Пароль - 'string'
    Числовые типы - нет

Атрибуты fixed и validate_rule можно задавать как кастомные атрибуты flask_mongoengine.
"""
from typing import Union, List, Type, Dict

import bson
import datetime

import mongoengine
from mongoengine.document import Document

ConvertedField = Dict[str, Union[str, int, List[str]]]
ConvertedDocument = List[ConvertedField]


def gen_field_row(text: str, name: str, type: str, opts: List[str] = None,
                  value: str='', fixed: bool=False, validate_rule: str="") -> ConvertedField:
    if opts is None:
        opts = []
    return {
        'text': text,
        'name': name,
        'type': type,
        'opts': opts,
        'value': value,
        'fixed': fixed,
        'validate_rule': validate_rule
    }


def convert_html_to_mongo_types(obj) -> str:
    """
    Переводит поля модели mongoDB в типы HTML
    :param obj: Поле mongoengine
    :return: Наиболее тип HTML
    """
    if isinstance(obj, mongoengine.fields.IntField):
        return 'number'
    if isinstance(obj, mongoengine.fields.DateTimeField):
        return 'date'
    try:
        if obj.validate == 'password':
            return 'password'
    except AttributeError:
        return 'text'
    # if obj.isinstance(mongoengine.fields.StringField):
    return 'text'


# noinspection PyProtectedMember
def convert_mongo_model(obj: Type[Document]) -> ConvertedDocument:
    """
    Конвертирует класс модели mongoengine
    :param obj: Модель mongoengine
    :return: Конвертированная модель
    """
    fields = obj._fields_ordered
    res = []
    for field in fields:
        # noinspection PyUnresolvedReferences
        current_field = obj._fields[field]
        try:
            text = current_field.verbose_name
        except AttributeError:
            text = '%NO_VERBOSE_NAME%'
        try:
            fixed = current_field.fixed
        except AttributeError:
            fixed = False
        try:
            validate_rule = current_field.validate_rule
        except AttributeError:
            validate_rule = ""
        name = current_field.name
        type = convert_html_to_mongo_types(current_field)
        opts = None
        if current_field.choices:
            opts = current_field.choices
        value = ''
        res.append(gen_field_row(text, name, type, opts, value, fixed, validate_rule))
    return res


def convert_mongo_document(obj: Document) -> ConvertedDocument:
    """
    Конвертирует документ
    :param obj: Документ
    :return: Конвертированный документ
    """
    res = convert_mongo_model(obj)
    # noinspection PyProtectedMember
    fields = obj._fields_ordered
    for i in range(len(fields)):
        data = obj[fields[i]]
        if isinstance(data, datetime.datetime):
            data = data.date().isoformat()
        if isinstance(data, bson.objectid.ObjectId):
            data = str(data)
        if isinstance(data, Document):
            data = str(data.id)
        res[i]['value'] = data
    return res
