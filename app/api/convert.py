from typing import Union, List, Type, Dict

import bson
import datetime

import mongoengine
from mongoengine.document import Document

ConvertedField = Dict[str, Union[str, int, List[str]]]
ConvertedDocument = List[ConvertedField]


def f(text: str, name: str, type: str, opts: List[str] = None,
      value: str='', fixed: bool =False) -> ConvertedField:
    if opts is None:
        opts = []
    return {
        'text': text,
        'name': name,
        'type': type,
        'opts': opts,
        'value': value,
        'fixed': fixed
    }


def convert_HTML_to_mongo_types(obj) -> str:
    if isinstance(obj, mongoengine.fields.IntField):
        return 'number'
    if isinstance(obj, mongoengine.fields.DateTimeField):
        return 'date'
    # if obj.isinstance(mongoengine.fields.StringField):
    return 'text'


# noinspection PyProtectedMember
def convert_mongo_model(obj: Type[Document]) -> ConvertedDocument:
    fields = obj._fields_ordered
    res = []
    for field in fields:
        current_field = obj._fields[field]
        try:
            text = current_field.verbose_name
        except AttributeError:
            text = '%NO_VERBOSE_NAME%'
        try:
            fixed = current_field.fixed
        except AttributeError:
            fixed = False
        name = current_field.name
        type = convert_HTML_to_mongo_types(current_field)
        opts = None
        if current_field.choices:
            opts = current_field.choices
        value = ''
        res.append(f(text, name, type, opts, value, fixed))
    return res


def convert_mongo_document(obj: Document) -> ConvertedDocument:
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
