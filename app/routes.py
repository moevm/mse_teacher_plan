from flask import render_template, url_for, request, jsonify
from app import app
from app import models_temp

f = models_temp.f

profile = [
    f('Фамилия', 'last_name', 'text', value='Корытов'),
    f('Имя', 'first_name', 'text', value='Павел'),
    f('Отчество', 'patronymic', 'text', value='Валерьевич'),
    f('Должность', 'type', 'text', opts=['Преподаватель', 'Администратор'], value='Администратор'),
    f('Год рождения', 'birth_date', 'date', value='1998-08-14'),
    f('Github id', 'github_id', 'number', value='12345'),
    f('Stepic id', 'stepic_id', 'number', value='67890'),
    f('Год вступления в должность', 'election_date', 'date', value='2010-05-05'),
    f('Дата переизбрания (окончание трудового договора)', 'contract_date', 'date', value='2012-06-30'),
    f('Учёная степень', 'academic_status', 'text',
      opts=['Ассистент', 'Старший преподаватель', 'Доцент', 'Профессор'],
      value='Ассистент'),
    f('Год присуждения', 'year_of_academic_status', 'number', value='2018')
]


@app.route('/')
@app.route('/index')
@app.route('/tpindex')
def index():
    return render_template('index.html', title='Главная', profile=profile)


@app.route('/newplan', methods=['POST'])
def add_new_plan():
    req_data = request.get_json()
    print(req_data)
    return jsonify({'ok': True, 'message': ''})


@app.route('/tpprofile')  # TODO
def tpprofile():
    return render_template('profile.html', title='Профиль', profile=profile)


@app.route('/tplogout')  # TODO
def tplogout():
    return 'DUMMY'


@app.route('/tpnewplan')  #TODO
def tpnewplan():
    return render_template('makeNewPlan.html', title='Новый план', models=models_temp.models)


@app.route('/tpplanlist')  #TODO
def tpplanlist():
    return 'DUMMY'


@app.route('/tpsimplereport')  #TODO
def tpsimplereport():
    return 'DUMMY'