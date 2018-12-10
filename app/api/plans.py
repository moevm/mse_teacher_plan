"""
========================
API для работы с планами
========================
"""
import random
from typing import List, Dict, Union, Tuple

from flask_mongoengine import Document

from app.api.users import get_available_users, get_user_by_id, get_profile_by_user_id
from app.api.convert import convert_mongo_document, convert_mongo_model, ConvertedDocument
from app.api.models import get_model_class_by_name, get_model_classes, get_model_info_by_name, get_models
# Новый план
from app.models.model import DocId


def new_plan(plan_type: str, plan):
    """
    Создание нового плана
    :param plan_type: Тип плана
    :param plan: Словарь с данными плана. [name: str]: str
    """
    model_class = get_model_class_by_name(plan_type)
    plan['model'] = get_model_info_by_name(plan_type)
    created_plan = model_class(**plan)
    created_plan.save()


def new_fake_plan(user_id: DocId, plan_type: str) -> Document:
    """
    Новый случайный план
    :param user_id: Id пользователя, для которого происходит генерация
    :param plan_type: Тип
    :return: Созданный план
    """
    model_class = get_model_class_by_name(plan_type)
    from app.models.fake.plan import generate_fake_by_converted_model
    plan = generate_fake_by_converted_model(convert_mongo_model(get_model_class_by_name(plan_type)))
    plan['model'] = get_model_info_by_name(plan_type)
    plan['user'] = get_user_by_id(user_id)
    created_plan = model_class(**plan)
    created_plan.save()
    return created_plan


def new_multiple_fake_plans(user_id: DocId, number: int):
    """
    Создание нескольких случайных планов
    :param user_id: Id пользователя, для которого происходит генерация
    :param number: Количество
    """
    model_types = [i['name'] for i in get_models()]
    for i in range(number):
        new_fake_plan(user_id, random.choice(model_types))


def save_plan(plan_id: DocId, plan_info):
    """
    Сохранение (или обновление) плана
    :param plan_id: Id плана
    :param plan_info: Словарь с информацией
    """
    plan = get_plan_document(plan_id)
    plan.modify(**plan_info)
    plan.save()


def get_plan_document(plan_id: DocId) -> Document:
    """
    Получение объекта документа mongoengine по id плана
    :param plan_id: Id плана
    :return: Документ mongoengine
    """
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            return plan
        except model.DoesNotExist:
            continue


def get_plan(plan_id: DocId) -> ConvertedDocument:
    """
    Получение конвертированного плана по Id
    """
    return convert_mongo_document(get_plan_document(plan_id))


def delete_plan(plan_id: DocId):
    """
    Удаление плана по Id
    :param plan_id: Id плана в БД
    """
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            plan.delete()
        except model.DoesNotExist:
            continue


def delete_user_plans(id):
    """
    Удалить все планы пользователя
    :param id: Id пользователя
    """
    for plan in get_user_plans(id):
        delete_plan(plan.id)


def get_user_plans(id: DocId = None) -> List[Document]:
    """
    Получить все планы пользователя
    :param id: Id пользователя
    :return: Список с документами mongoengine
    """
    models = get_model_classes()
    res = []
    for model in models:
        if id is not None:
            plans = model.objects(user=id)
        else:
            plans = model.objects
        for plan in plans:
            res.append(plan)
    return res


def get_converted_user_plans(id: DocId = None, year_start: int = 0, year_end: int = 3000)\
        -> List[Dict[str, Union[list, ConvertedDocument]]]:
    """
    Получить конвертированные планы пользователя. Если id - None, то планы всех пользователей
    :param id: Id пользователя
    :param year_start: Год начала
    :param year_end: Год окончания
    """
    models = get_model_classes()
    res = []
    for model in models:
        if id is not None:
            plans = model.objects(user=id)
        else:
            plans = model.objects()
        if len(plans) != 0:
            current_res = {
                'name': plans[0].model.name,
                'text': plans[0].model.text,
                'plans': []
            }
            for plan in plans:
                if year_start <= plan.year <= year_end:
                    current_res['plans'].append(convert_mongo_document(plan))
            res.append(current_res)
    return res


def get_plans_stat(id: DocId = None, year_start: int = 0, year_end: int = 3000)\
        -> Tuple[List[Dict[str, Union[str, int]]], int]:
    """
    Получить статистику по планам
    Возвращаемый объект:
    (
        [
            {
                'name' - тип плана
                'plans_num' - количество планов этого типа
            },
        ]
        Общее число планов
    )
    :param id: Id пользователя
    :param year_start: Год начала
    :param year_end: Год окончания
    """
    plans = get_converted_user_plans(id, year_start, year_end)
    res = []
    total = 0
    for plan_type in plans:
        plan_info = {
            'name': plan_type['text'],
            'plans_num': len(plan_type['plans'])
        }
        total = total + len(plan_type['plans'])
        res.append(plan_info)
    return res, total


def get_converted_available_plans(id, year_start, year_end) -> List[ConvertedDocument]:
    """
    Получить конвертированные планы, доступ к которым есть у пользоватеоя
    :param id: Id пользователя
    :param year_start: Год начала
    :param year_end: Год окончания
    :return: Список с конвертированными планами
    """
    def is_already_saved(_all, _plan_group):
        _already_saved = None
        for saved_plan_group in _all:
            if _plan_group['name'] == saved_plan_group['name']:
                _already_saved = saved_plan_group
                break
        return _already_saved

    def set_verbose_user(_plan_group):
        for _plan in _plan_group['plans']:
            _id = _plan[1]['value']
            profile = get_profile_by_user_id(_id)
            _plan[1]['text'] = 'Пользователь'
            _plan[1]['value'] = profile.last_name + ' ' + profile.first_name
        return _plan_group

    all = []
    for user in get_available_users(get_user_by_id(id)):
        current_plans = get_converted_user_plans(user.id, year_start, year_end)
        for plan_group in current_plans:
            already_saved = is_already_saved(all, plan_group)
            if already_saved is not None:
                for plan in plan_group['plans']:
                    already_saved['plans'].append(plan)
            else:
                all.append(plan_group)
    for plan_group in all:
        set_verbose_user(plan_group)
    return all
