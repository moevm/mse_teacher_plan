import importlib

from flask import render_template, url_for, request, jsonify, redirect
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.models.model import Model
from app.models.profile import Profile
from app.models.user import User
from app.convert import *


def f(text, name, type, opts=None, value=''):
    if opts is None:
        opts = []
    return {'text': text, 'name': name, 'type': type, 'opts': opts, 'value': value}


def get_current_profile():
    for c_user in Profile.objects(user=current_user.id):
        return c_user
    return None


def get_model_class_by_name(name):
    model = Model.objects.get(name=name)
    module = importlib.import_module("app.models." + model.fileName, model.className)
    model_class = getattr(module, model.className)
    return model_class


def get_models():
    def m(text, name, fields):
        return {'text': text, 'name': name, 'fields': fields}
    res = []
    for model in Model.objects:
        module = importlib.import_module("app.models." + model.fileName, model.className)
        model_class = getattr(module, model.className)
        res.append(m(model.text, model.name, convert_mongo_model(model_class)))
    return res


# Логин
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def check_login():
    req_data = request.get_json()
    try:
        found_user = User.objects.get(login=req_data['login'])
    except User.DoesNotExist:
        return jsonify({"ok": False, 'data': 'Логил или пароль неверны'})
    if found_user is not None and found_user.check_password(req_data['password']):
        login_user(found_user)
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, 'data': 'Логил или пароль неверны'})


# Регистрация
@app.route('/registration')
def registration():
    profile = [
                  f('Логин', 'login', 'text'),
                  f('Пароль', 'password', 'text')
              ] + convert_mongo_model(Profile)
    return render_template('registration.html', profile=profile)


@app.route('/registration', methods=['POST'])
def new_profile():
    req_data = request.get_json()
    user = User(
        login=req_data['login']
    )
    user.set_password(req_data['password'])
    del req_data['login']
    del req_data['password']
    profile = Profile(user=user, **req_data)
    user.save()
    profile.save()
    return jsonify({"ok": True})


# Обновление профиля
@app.route('/profile', methods=['PUT'])
def update_profile():
    req_data = request.get_json()
    # user = User.objects.get(id=req_data['user'])
    del req_data['user']
    profile = Profile.objects.get(id=req_data['id'])
    del req_data['id']
    for entry in req_data:
        profile[entry] = req_data[entry]
    profile.save()
    return jsonify({"ok": True})


@app.route('/')
@app.route('/index')
@app.route('/tpindex')
@login_required
def index():
    return render_template('index.html', title='Главная', profile=get_current_profile())


@app.route('/newplan', methods=['POST'])
@login_required
def add_new_plan():
    req_data = request.get_json()
    model_class = get_model_class_by_name(req_data['add_info'])
    del req_data['add_info']
    new_plan = model_class(**req_data)
    new_plan.save()
    return jsonify({'ok': True, 'message': ''})


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


@app.route('/tpnewplan')  # TODO Refactor?
@login_required
def tpnewplan():
    models = get_models()
    return render_template('makeNewPlan.html', title='Новый план', models=models)


@app.route('/tpplanlist')  #TODO
@login_required
def tpplanlist():
    return 'DUMMY'


@app.route('/tpsimplereport')  #TODO
@login_required
def tpsimplereport():
    return 'DUMMY'
