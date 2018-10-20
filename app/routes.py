from flask import render_template, url_for, request, jsonify
from app import app, db
from app import models_temp
from app.models.user import User

f = models_temp.f

pavel = None
for user in User.objects(first_name='Павел'):
    pavel = user


@app.route('/')
@app.route('/index')
@app.route('/tpindex')
def index():
    return render_template('index.html', title='Главная', profile=pavel)


@app.route('/newplan', methods=['POST'])
def add_new_plan():
    req_data = request.get_json()
    print(req_data)
    return jsonify({'ok': True, 'message': ''})


@app.route('/tpprofile')  # TODO
def tpprofile():
    return render_template('profile.html', title='Профиль', profile=pavel)


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