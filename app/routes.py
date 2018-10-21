from flask import render_template, url_for, request, jsonify
from app import app, db
from app import models_temp
from app.models.user import User
from app.models.books import Book
from app.convert import *


def f(text, name, type, opts=None, value=''):
    if opts is None:
        opts = []
    return {'text': text, 'name': name, 'type': type, 'opts': opts, 'value': value}


def m(text, name, fields):
    return {'text': text, 'name': name, 'fields': fields}


models = [
    m('Подготовка учебников', 'books', convert_mongo_template(Book))
]

pavel = None  # TODO
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


@app.route('/tpprofile')
def tpprofile():
    return render_template('profile.html', title='Профиль', profile=convert_mongo_document(pavel))


@app.route('/tplogout')  # TODO
def tplogout():
    return 'DUMMY'


@app.route('/tpnewplan')  #TODO
def tpnewplan():
    return render_template('makeNewPlan.html', title='Новый план', models=models)


@app.route('/tpplanlist')  #TODO
def tpplanlist():
    return 'DUMMY'


@app.route('/tpsimplereport')  #TODO
def tpsimplereport():
    return 'DUMMY'