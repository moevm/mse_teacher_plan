from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from api.models import get_models
from api.plans import new_plan, delete_plan, get_plan, save_plan, get_converted_user_plans, \
    get_converted_available_plans
from api.users import get_available_profiles, get_current_profile
from app import app


@app.route('/tpnewplan')
@login_required
def tpnewplan():
    models = get_models()
    return render_template('makeNewPlan.html', title='Новый план', models=models, user=get_current_profile())


@app.route('/tpplanlist')
@login_required
def tpplanlist():
    return render_template('listOfPlans.html', title='Список планов', user=get_current_profile(),
                           available_users=get_available_profiles(current_user))


@app.route('/newplan', methods=['POST'])
@login_required
def add_new_plan():
    req_data = request.get_json()
    req_data['year'] = req_data['add_info']['year']
    req_data['user'] = current_user.id
    plan_type = req_data['add_info']['type']
    del req_data['add_info']
    new_plan(plan_type, req_data)
    return jsonify({'ok': True, 'message': ''})


@app.route('/plan', methods=['DELETE'])
@login_required
def delete_plan_req():
    req_data = request.get_json()
    delete_plan(req_data['id'])
    return jsonify({'ok': True, 'message': ''})


@app.route('/plan', methods=['GET'])
@login_required
def get_plan_req():
    req_data = request.args
    plan = get_plan(req_data['id'])
    return render_template('editPlan.html', title='Редактиование плана', plan=plan, user=get_current_profile())


@app.route('/plan', methods=['PUT'])
@login_required
def edit_plan():
    req_data = request.get_json()
    del req_data['user']
    del req_data['model']  # TODO Delete possible unnecessary iteration through DB
    plan_id = req_data['id']
    del req_data['id']
    save_plan(plan_id, req_data)
    return jsonify({'ok': True})


@app.route('/plans', methods=['GET'])
@login_required
def plans():
    req_data = request.args
    if req_data['user_id'] != 'All':
        plans = get_converted_user_plans(req_data['user_id'], int(req_data['year_start']), int(req_data['year_end']))
    else:
        plans = get_converted_available_plans(current_user.id, int(req_data['year_start']), int(req_data['year_end']))
    return jsonify({'ok': True, 'plans': plans})