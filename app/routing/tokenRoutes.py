from app.api.users import get_current_profile
from flask_login import login_required, current_user

from app.api.tokens import *
from app.routing.userTypeDecorators import manager_required
from app import app
from flask import render_template, request, jsonify


@app.route('/tokens')
@login_required
@manager_required
def tokens():
    return render_template('token.html', title='Выдача токенов',
                           tokens=get_available_token_types(current_user.id),
                           user=get_current_profile())


@app.route('/token', methods=['POST'])
@login_required
@manager_required
def token():
    req_data = request.get_json()
    token_type = req_data['type']
    if check_token_availability(current_user.id, token_type):
        token_key = get_new_token(token_type)
        return jsonify({"ok": True, 'key': token_key})
    return jsonify({"ok": False, "message": 'Неверен тип токена'})
