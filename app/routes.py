from flask import render_template, url_for, request, jsonify, redirect
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.api.models import *
from app.api.plans import *
from app.api.users import *


def get_current_profile():
    return get_profile_by_user_id(current_user.id)


# Логин
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def check_login():
    req_data = request.get_json()
    found_user = check_user_auth(req_data)
    if found_user is None:
        return jsonify({"ok": False, 'data': 'Логин или пароль неверны'})
    else:
        login_user(found_user)
        return jsonify({"ok": True})


# Регистрация
@app.route('/registration')
def registration():
    return render_template('registration.html', profile=get_registration_form())


@app.route('/registration', methods=['POST'])
def new_profile():
    req_data = request.get_json()
    try:
        register_user(req_data)
    except Exception as exp:  # TODO process common exceptions
        return jsonify({"ok": False, 'data': type(exp)})
    return jsonify({"ok": True})


# Обновление профиля
@app.route('/profile', methods=['PUT'])
def upd_profile():
    req_data = request.get_json()
    update_profile(req_data)
    return jsonify({"ok": True})


@app.route('/')
@app.route('/index')
@app.route('/tpindex')
@login_required
def index():
    return render_template('index.html', title='Главная', profile=get_current_profile())


@app.route('/tpprofile')
@login_required
def tpprofile():
    return render_template('profile.html', title='Профиль',
                           profile=convert_mongo_document(get_current_profile()))


@app.route('/tplogout')
@login_required
def tplogout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/newplan', methods=['POST'])
@login_required
def add_new_plan():
    req_data = request.get_json()
    req_data['year'] = req_data['add_info']['year']
    plan_type = req_data['add_info']['type']
    del req_data['add_info']
    new_plan(plan_type, req_data)
    return jsonify({'ok': True, 'message': ''})


@app.route('/tpnewplan')
@login_required
def tpnewplan():
    models = get_models()
    return render_template('makeNewPlan.html', title='Новый план', models=models)


@app.route('/plans', methods=['GET'])  # TODO
@login_required
def plans():
    req_data = request.get_json()
    get_user_plans(req_data['user_id'])
    return jsonify({'ok': True, 'message': ''})

@app.route('/tpplanlist')
@login_required
def tpplanlist():
    return render_template('listOfPlans.html', title='Список планов', profile=get_current_profile(),
                           available_users=get_available_users(current_user))


@app.route('/tpsimplereport')  #TODO
@login_required
def tpsimplereport():
    return 'DUMMY'
