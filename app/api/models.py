import importlib
from typing import List

from app.api.convert import *
from app.models.model import Model


def get_model_class_by_name(name):
    model = Model.objects.get(name=name)
    module = importlib.import_module("app.models." + model.fileName, model.className)
    model_class = getattr(module, model.className)
    return model_class


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


def get_models():
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

