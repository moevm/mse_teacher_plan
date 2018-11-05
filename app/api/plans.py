from flask_mongoengine import Document

from app.api.convert import convert_mongo_document
from app.api.models import get_model_class_by_name, get_model_classes, get_model_names, get_model_info_by_name


# Новый план
def new_plan(plan_type, plan):
    model_class = get_model_class_by_name(plan_type)
    plan['model'] = get_model_info_by_name(plan_type)
    created_plan = model_class(**plan)
    created_plan.save()


def save_plan(plan_id, plan_info):
    plan = get_plan_document(plan_id)
    plan.modify(**plan_info)
    plan.save()


def get_plan_document(plan_id):
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            return plan
        except model.DoesNotExist:
            continue


def get_plan(plan_id):
    return convert_mongo_document(get_plan_document(plan_id))


def delete_plan(plan_id):
    models = get_model_classes()
    for model in models:
        try:
            plan = model.objects.get(id=plan_id)
            plan.delete()
        except model.DoesNotExist:
            continue


# Получить планы пользователя
def get_user_plans(id, year_start, year_end):
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
