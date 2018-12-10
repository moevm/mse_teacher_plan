"""
=========================
API для работы с моделями
=========================
Модели - классы mongoengine. Информация о них хранится в БД. На основе информации происходит
динамическое подключение
"""
import importlib
from typing import List, Type

import logging

from app.api.convert import *
from app.models.model import Model

models_path = "app.models.plans."


def get_model_class_by_name(name: str) -> Type[mongoengine.Document]:
    """
    Получит класс модели по имени
    :param name: Имя
    :return: Класс модели
    """
    model = Model.objects.get(name=name)
    module = importlib.import_module(models_path + model.fileName, model.className)
    model_class = getattr(module, model.className)
    return model_class


def get_model_info_by_name(name: str) -> mongoengine.QuerySet:
    """
    Получение объекта с информацией о модели по имени модели
    :param name: Имя модели
    :return: Объект с информацией (документ mongoengine)
    """
    model = Model.objects.get(name=name)
    return model


def get_model_classes() -> List[Document]:
    """
    Получить список из классов всех моделей. Используется для динамического подключения моделей
    :return:
    """
    res = []
    for model in Model.objects:
        try:
            module = importlib.import_module(models_path + model.fileName, model.className)
            model_class = getattr(module, model.className)
            res.append(model_class)
        except ModuleNotFoundError:
            logging.error(f'Модуль "{model.text}" не найден')
    return res


def get_model_names() -> List[str]:
    """
    Получить список имён моделей
    :return:
    """
    res = []
    for model in Model.objects:
        res.append(model.name)
    return res


def get_models() -> List[Dict[str, str]]:
    """
    Получить конвертированные модели. Может применятся, например, при составлении форм
    :return:
    """
    def m(text, name, fields):
        return {'text': text, 'name': name, 'fields': fields}
    res = []
    for model in Model.objects:
        try:
            module = importlib.import_module(models_path + model.fileName, model.className)
            model_class = getattr(module, model.className)
            res.append(m(model.text, model.name, convert_mongo_model(model_class)))
        except ModuleNotFoundError:
            logging.error(f'Модуль "{model.text}" не найден')
    return res

