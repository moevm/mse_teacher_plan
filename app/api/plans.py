from app.api.models import get_model_class_by_name, get_model_classes


# Новый план
def new_plan(plan_type, plan):
    model_class = get_model_class_by_name(plan_type)
    created_plan = model_class(**plan)
    created_plan.save()


def get_user_plans(id):
    models = get_model_classes()
    for model_class in models:
        plans = model_class.objects.get(user=id)
        for plan in plans:
            print(plan)