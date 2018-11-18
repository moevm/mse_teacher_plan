import importlib
from typing import List, Type

from app.api.convert import *
from app.models.model import Model


def get_model_class_by_name(name: str) -> Type[mongoengine.Document]:
    model = Model.objects.get(name=name)
    module = importlib.import_module("app.models." + model.fileName, model.className)
    model_class = getattr(module, model.className)
    return model_class


def get_model_info_by_name(name: str) -> mongoengine.QuerySet:
    model = Model.objects.get(name=name)
    return model


def get_model_classes() -> List[Document]:
    res = []
    for model in Model.objects:
        try:
            module = importlib.import_module("app.models." + model.fileName, model.className)
            model_class = getattr(module, model.className)
            res.append(model_class)
        except ModuleNotFoundError:
            print(f'Модуль "{model.text}" не найден')
    return res


def get_model_names() -> List[str]:
    res = []
    for model in Model.objects:
        res.append(model.name)
    return res


def get_models() -> List[Dict[str, str]]:
    def m(text, name, fields):
        return {'text': text, 'name': name, 'fields': fields}
    res = []
    for model in Model.objects:
        try:
            module = importlib.import_module("app.models." + model.fileName, model.className)
            model_class = getattr(module, model.className)
            res.append(m(model.text, model.name, convert_mongo_model(model_class)))
        except ModuleNotFoundError:
            print(f'Модуль "{model.text}" не найден')
    return res

