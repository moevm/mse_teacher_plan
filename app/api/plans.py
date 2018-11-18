from typing import List

from flask_mongoengine import Document

from api.users import get_available_users, get_user_by_id, get_profile_by_user_id
from app.api.convert import convert_mongo_document, convert_mongo_model, ConvertedDocument
from app.api.models import get_model_class_by_name, get_model_classes, get_model_info_by_name
# Новый план
from models.fake.plan import generate_fake_by_converted_model
from models.model import DocId


def new_plan(plan_type: str, plan):
    model_class = get_model_class_by_name(plan_type)
    plan['model'] = get_model_info_by_name(plan_type)
    created_plan = model_class(**plan)
    created_plan.save()


def new_fake_plan(user_id: DocId, plan_type: str) -> Document:
    model_class = get_model_class_by_name(plan_type)
    plan = generate_fake_by_converted_model(convert_mongo_model(get_model_class_by_name(plan_type)))
    plan['model'] = get_model_info_by_name(plan_type)
    plan['user'] = get_user_by_id(user_id)
    created_plan = model_class(**plan)
    created_plan.save()
    return created_plan


def save_plan(plan_id: DocId, plan_info):
    plan = get_plan_document(plan_id)
    plan.modify(**plan_info)
    plan.save()


def get_plan_document(plan_id: DocId) -> Document:
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            return plan
        except model.DoesNotExist:
            continue


def get_plan(plan_id: DocId) -> ConvertedDocument:
    return convert_mongo_document(get_plan_document(plan_id))


def delete_plan(plan_id: DocId):
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            plan.delete()
        except model.DoesNotExist:
            continue


# Получить планы пользователя
def get_user_plans(id: DocId, year_start: int, year_end: int) -> List[ConvertedDocument]:
    models = get_model_classes()
    res = []
    for model in models:
        plans = model.objects(user=id)
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


def get_available_plans(id, year_start, year_end) -> List[ConvertedDocument]:
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
        current_plans = get_user_plans(user.id, year_start, year_end)
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
