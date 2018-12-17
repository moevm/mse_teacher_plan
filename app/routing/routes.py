"""
=============
Маршрутизация
=============
Модуль routing отвечает за маршрутизацию запросов от пользователя в приложении.
Маршруты разбиты на файлы по функциям:
    fakeDataRoutes - генерация фейковых данных
    plansRoutes - работа с планами
    profileRoutes - работа с профилями
    registrationRoutes - авторизация и регистрация пользователей
    reportRoutes - работа с PDF-отчётам
    tokenRoutes - выдача токенов
    userListRoutes - работа со списком пользователей
"""
from flask import render_template
from flask_login import login_required

from app import app

# noinspection PyUnresolvedReferences
from app.routing import fakeDataRoutes, plansRoutes, profileRoutes, registrationRoutes, reportRoutes, userListRoutes,\
    tokenRoutes
from app.api.users import get_current_profile
from app.routing.userTypeDecorators import admin_required


# Главная страница
@app.route('/')
@app.route('/index')
@app.route('/tpindex')
@login_required
def index():
    return render_template('index.html', title='Главная', user=get_current_profile())


# Логи
@app.route('/logs')
@login_required
@admin_required
def logs():
    return render_template('logs.html', title='Логи', user=get_current_profile())

