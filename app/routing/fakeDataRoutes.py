from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from app.api.models import get_models
from app.api.plans import new_fake_plan
from app.api.users import get_available_profiles, register_multiple_fake_users, get_current_profile
from app import app
from app.routing.userTypeDecorators import admin_required


@app.route('/tpfillbd')
@login_required
@admin_required
def tpfillbd():
    models = get_models()
    return render_template('fillDatabase.html', title='Заполнение БД', user=get_current_profile(),
                           available_users=get_available_profiles(current_user), models=models)


@app.route('/fakeplan', methods=['POST'])
@login_required
@admin_required
def fake_plan():
    req_data = request.get_json()
    new_fake_plan(req_data['user_id'], req_data['type'])
    return jsonify({'ok': True})


@app.route('/fakedata', methods=['POST'])
@login_required
@admin_required
def fake_data():
    req_data = request.get_json()
    register_multiple_fake_users(int(req_data['users']), int(req_data['plans']))
    return jsonify({'ok': True})
