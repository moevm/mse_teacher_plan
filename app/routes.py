from flask import render_template, url_for, request, jsonify, redirect
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.models.profile import Profile
from app.models.books import Book
from app.convert import *
from app.models.user import User


def f(text, name, type, opts=None, value=''):
    if opts is None:
        opts = []
    return {'text': text, 'name': name, 'type': type, 'opts': opts, 'value': value}


def m(text, name, fields):
    return {'text': text, 'name': name, 'fields': fields}


def get_current_profile():
    for c_user in Profile.objects(user=current_user.id):
        return c_user
    return None


models = [
    m('Подготовка учебников', 'books', convert_mongo_template(Book))
]


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def check_login():
    req_data = request.get_json()
    found_user = None
    for user in User.objects(login=req_data['login']):
        found_user = user
    if found_user is not None and found_user.check_password(req_data['password']):
        login_user(found_user)
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, 'data': 'Логил или пароль неверны'})


@app.route('/registration')
def registration():
    profile = [
        f('Логин', 'login', 'text'),
        f('Пароль', 'password', 'text')
    ] + convert_mongo_template(Profile)
    return render_template('registration.html', profile=profile)


@app.route('/registration', methods=['POST'])
def new_profile():
    req_data = request.get_json()
    user = User(
        login=req_data['login']
    )
    user.set_password(req_data['password'])
    profile = Profile(
        user=user,
        last_name=req_data['last_name'],
        first_name=req_data['first_name'],
        patronymic=req_data['patronymic'],
        type=req_data['type'],
        birth_date=req_data['birth_date'],
        github_id=req_data['github_id'],
        stepic_id=req_data['stepic_id'],
        election_date=req_data['election_date'],
        contract_date=req_data['contract_date'],
        academic_status=req_data['academic_status'],
        year_of_academic_status=req_data['year_of_academic_status']
    )
    user.save()
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
    print(req_data)
    return jsonify({'ok': True, 'message': ''})


@app.route('/tpprofile')
@login_required
def tpprofile():
    return render_template('profile.html', title='Профиль',
                           profile=convert_mongo_document(get_current_profile()))


@app.route('/tplogout')  # TODO
@login_required
def tplogout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tpnewplan')  #TODO
@login_required
def tpnewplan():
    return render_template('makeNewPlan.html', title='Новый план', models=models)


@app.route('/tpplanlist')  #TODO
@login_required
def tpplanlist():
    return 'DUMMY'


@app.route('/tpsimplereport')  #TODO
@login_required
def tpsimplereport():
    return 'DUMMY'