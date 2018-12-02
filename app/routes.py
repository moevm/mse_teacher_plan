from datetime import datetime as dt

import pdfkit
from flask import render_template, url_for, request, jsonify, redirect, send_file
from flask_login import current_user, login_user, logout_user, login_required

from app.api.plans import *
from app.api.users import *
from app import app


def get_current_profile():
    return get_profile_by_user_id(current_user.id)


def get_report_info(type_of_report):
    prof = get_current_profile()
    info = {
        'time': dt.now().strftime('%H:%M:%S'),
        'date': dt.now().strftime('%Y-%m-%d'),
        'creator': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic,
        'type': type_of_report
    }
    return info


def get_available_report_types():
    user = get_current_profile()
    res = [{
        'text': 'Статистика по пользователю',
        'name': 'user_stats'
    }]
    if user.type != 'Преподаватель':
        res.append({
            'text': 'Статистика по кафедре',
            'name': 'all_stats'
        })
    return res


def get_stat_report_template():
    info = get_report_info('Статистика по кафедре')
    plans_stat, total_plans = get_plans_stat()
    table_stats = [
        {
            'name': 'Общее количество пользователей',
            'value': count_users()
        },
        {
            'name': 'Общее количество планов',
            'value': total_plans
        }
    ]
    user_categs = count_user_categs()
    users_list = get_user_and_profile_list()
    users = [user['profile'] for user in users_list]
    return render_template('reports/statistic.html', info=info, stats=table_stats, plans=plans_stat,
                           user_categs=user_categs, users=users)


def get_user_stat_report_template(user_id):
    info = get_report_info('Статистика пользователя')
    if not user_id:
        user_id = current_user.id
    prof = get_profile_by_user_id(user_id)
    plans_stat, total_plans = get_plans_stat(user_id)
    plans_list = get_converted_user_plans(user_id)
    table_stats = [{
        'name': 'Пользователь',
        'value': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic
    },
        {
            'name': 'Общее количество планов',
            'value': total_plans
        }
    ]
    return render_template('reports/user_stats.html', info=info, stats=table_stats, plans=plans_stat,
                           plans_list=plans_list)

# Логин
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def check_login():
    req_data = request.get_json()
    import pymongo
    try:
        found_user = check_user_auth(req_data)
        if found_user is None:
            return jsonify({"ok": False, 'data': 'Логин или пароль неверны'})
        else:
            login_user(found_user)
            return jsonify({"ok": True})
    except pymongo.errors.ServerSelectionTimeoutError:
        return jsonify({"ok": False, 'data': 'MongoDB не запущен'})


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
        return jsonify({"ok": False, 'data': exp.args})
    return jsonify({"ok": True})


# Обновление профиля
@app.route('/profile', methods=['PUT'])
def upd_profile():
    req_data = request.get_json()
    update_profile(req_data)
    return jsonify({"ok": True})


@app.route('/user', methods=['DELETE'])
@login_required
def delete_user_req():
    req_data = request.get_json()
    if str(current_user.id) == req_data['id']:
        logout_user()
        delete_user(req_data['id'])
        return jsonify({'ok': True, 'reload': True, 'message': ''})
    else:
        delete_user(req_data['id'])
        return jsonify({'ok': True, 'reload': False, 'message': ''})


@app.route('/password', methods=['PUT'])
@login_required
def change_pass():
    req_data = request.get_json()
    res = change_password(current_user.id, req_data['old_pass'], req_data['new_pass'])
    if res:
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False, 'message': 'Old password is incorrect'})


@app.route('/')
@app.route('/index')
@app.route('/tpindex')
@login_required
def index():
    return render_template('index.html', title='Главная', user=get_current_profile())


@app.route('/tpprofile')
@login_required
def tpprofile():
    return render_template('profile.html', title='Профиль',
                           profile=convert_mongo_document(get_current_profile()), user=get_current_profile())


@app.route('/tplogout')
@login_required
def tplogout():
    logout_user()
    return redirect(url_for('index'))


# Новый план
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


@app.route('/fakeplan', methods=['POST'])
@login_required
def fake_plan():
    req_data = request.get_json()
    new_fake_plan(req_data['user_id'], req_data['type'])
    return jsonify({'ok': True})


@app.route('/fakedata', methods=['POST'])
@login_required
def fake_data():
    req_data = request.get_json()
    register_multiple_fake_users(int(req_data['users']), int(req_data['plans']))
    return jsonify({'ok': True})


@app.route('/tpnewplan')
@login_required
def tpnewplan():
    models = get_models()
    return render_template('makeNewPlan.html', title='Новый план', models=models, user=get_current_profile())


@app.route('/plans', methods=['GET'])
@login_required
def plans():
    req_data = request.args
    if req_data['user_id'] != 'All':
        plans = get_converted_user_plans(req_data['user_id'], int(req_data['year_start']), int(req_data['year_end']))
    else:
        plans = get_converted_available_plans(current_user.id, int(req_data['year_start']), int(req_data['year_end']))
    return jsonify({'ok': True, 'plans': plans})


@app.route('/tpplanlist')
@login_required
def tpplanlist():
    return render_template('listOfPlans.html', title='Список планов', user=get_current_profile(),
                           available_users=get_available_profiles(current_user))


@app.route('/tpreport')
@login_required
def tpreport():
    return render_template('generateReport.html', title='Отчёт', user=get_current_profile(),
                           available_users=get_available_profiles(current_user))


@app.route('/reporttypes')
@login_required
def reporttypes():
    return jsonify({'ok': True, 'types': get_available_report_types()})


@app.route('/report')
@login_required
def report():
    req_data = request.args
    return get_report_html(req_data)


@app.route('/reportToPdf')
@login_required
def reportToPdf():
    req_data = request.args
    html = get_report_html(req_data)
    import random
    filename = ''
    for i in range(15):
        filename = filename + str(random.choice("0123456789ABCDEF"))
    filename = filename + '.pdf'
    actual_filename = 'app/static/generated_reports/' + filename
    pdfkit.from_string(html, actual_filename)
    url = url_for('static', filename=f'generated_reports/{filename}')
    return jsonify({'ok': True, 'url': url})


def get_report_html(req_data):
    if req_data['type'] == 'all_stats':
        return get_stat_report_template()
    if req_data['type'] == 'user_stats':
        if req_data['user_id'] == 'All':
            req_data['user_id'] = None
        return get_user_stat_report_template(req_data['user_id'])
    return 'TODO?'


@app.route('/tpfillbd')
@login_required
def tpfillbd():
    models = get_models()
    return render_template('fillDatabase.html', title='Заполнение БД', user=get_current_profile(),
                           available_users=get_available_profiles(current_user), models=models)


@app.route('/tpuserlist')
@login_required
def tpuserlist():
    return render_template('listOfUsers.html', title='Список пользователей', user=get_current_profile())


@app.route('/userlist', methods=['GET'])
@login_required
def userlist():
    return jsonify({'ok': True, 'users': get_user_and_profile_list()})
