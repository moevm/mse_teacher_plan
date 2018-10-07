from flask import render_template, url_for
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'isactive': True, 'last_name': 'Korytov', 'first_name': 'Pavel'}  # TODO
    profile = {'patronymic': 'Hmm'}
    return render_template('index.html', title='Home', user=user, profile=profile)


@app.route('/tpindex')  # TODO
def tpindex():
    return 'DUMMY'


@app.route('/tpprofile')  # TODO
def tpprofile():
    return 'DUMMY'


@app.route('/tplogout')  # TODO
def tplogout():
    return 'DUMMY'


@app.route('/tpnewplan')  #TODO
def tpnewplan():
    return 'DUMMY'


@app.route('/tpplanlist')  #TODO
def tpplanlist():
    return 'DUMMY'


@app.route('/tpsimplereport')  #TODO
def tpsimplereport():
    return 'DUMMY'