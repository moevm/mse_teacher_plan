import logging

from flask import url_for, render_template, request, jsonify
from flask_login import current_user, login_user
from werkzeug.utils import redirect

from app.api.users import check_user_auth, get_registration_form, register_user
from app import app


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
        logging.error(exp)
        return jsonify({"ok": False, 'data': exp.args})
    return jsonify({"ok": True})
