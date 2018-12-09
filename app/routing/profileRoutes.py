from app.api.users import get_profile_by_user_id, get_current_profile

from app.api.convert import convert_mongo_document
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user

from app.api.users import update_profile, delete_user, change_password
from app import app


# Обновление профиля
from routing.userTypeDecorators import admin_required


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


@app.route('/profile_edit')
@login_required
@admin_required
def profile_edit():
    req_data = request.args
    profile = convert_mongo_document(get_profile_by_user_id(req_data['user_id']))
    return render_template('profile.html', title='Редактирование профиля', profile=profile,
                           user=get_current_profile(), enable_fixed_edit=True)


@app.route('/password', methods=['PUT'])
@login_required
def change_pass():
    req_data = request.get_json()
    res = change_password(current_user.id, req_data['old_pass'], req_data['new_pass'])
    if res:
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False, 'message': 'Old password is incorrect'})


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
