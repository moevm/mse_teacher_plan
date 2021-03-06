from flask import render_template, jsonify
from flask_login import login_required

from app.api.users import get_user_and_profile_list, get_current_profile
from app import app
from app.routing.userTypeDecorators import manager_required


@app.route('/tpuserlist')
@login_required
@manager_required
def tpuserlist():
    return render_template('listOfUsers.html', title='Список пользователей', user=get_current_profile())


@app.route('/userlist', methods=['GET'])
@login_required
@manager_required
def userlist():
    return jsonify({'ok': True, 'users': get_user_and_profile_list()})
