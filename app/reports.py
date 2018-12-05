from datetime import datetime as dt
from typing import Dict, Any, List

import pdfkit
from flask import url_for, render_template
from flask_login import current_user

from app.api.plans import get_converted_user_plans, get_plans_stat
from app.api.reports import get_available_reports
from app.api.users import get_profile_by_user_id, count_user_categs, get_user_and_profile_list, count_users
from app.api.users import get_current_profile
from app.models.model import DocId


class ReportConstructor:
    arguments: Dict[str, Any]
    units: List[str]
    creator_id: DocId
    user_id: DocId

    def __init__(self, creator_id: DocId, user_id: DocId):
        self.user_id = user_id
        creator = get_profile_by_user_id(creator_id)
        info = {
            'time': dt.now().strftime('%H:%M:%S'),
            'date': dt.now().strftime('%Y-%m-%d'),
            'creator': creator.last_name + ' ' + creator.first_name + ' ' + creator.patronymic,
            'type': 'Конструированный отчёт'
        }
        self.arguments = {'info': info}
        self.units = []

    def add_user_plan(self):
        plans_list = get_converted_user_plans(self.user_id)
        self.arguments['plans_list'] = plans_list
        self.units.append('user_plan')

    def add_user_stats(self):
        prof = get_profile_by_user_id(self.user_id)
        plans_stat, total_plans = get_plans_stat(self.user_id)
        user_stats = [{
            'name': 'Пользователь',
            'value': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic
        },
            {
                'name': 'Общее количество планов',
                'value': total_plans
            }
        ]
        self.arguments['user_stats'] = user_stats
        self.arguments['user_plans_count'] = plans_stat
        self.units.append('user_stats')

    def add_users_categs(self):
        users_categs = count_user_categs()
        self.arguments['users_categs'] = users_categs
        self.units.append('users_categs')

    def add_plans_stats(self):
        plans_stat, total_plans = get_plans_stat()
        self.arguments['all_plans_count'] = plans_stat
        self.units.append('plans_stats')

    def add_users_list(self):
        users_and_profiles = get_user_and_profile_list()
        users_list = [user['profile'] for user in users_and_profiles]
        self.arguments['users_list'] = users_list
        self.units.append('users_list')

    def add_all_stats(self):
        plans_stat, total_plans = get_plans_stat()
        all_stats = [
            {
                'name': 'Общее количество пользователей',
                'value': count_users()
            },
            {
                'name': 'Общее количество планов',
                'value': total_plans
            }
        ]
        self.arguments['all_stats'] = all_stats
        self.units.append('all_stats')

    def get_html(self):
        return render_template('reports/combined_report.html', units=self.units, **self.arguments)


def get_report_info(type_of_report):
    prof = get_current_profile()
    info = {
        'time': dt.now().strftime('%H:%M:%S'),
        'date': dt.now().strftime('%Y-%m-%d'),
        'creator': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic,
        'type': type_of_report
    }
    return info


def get_available_report_units():
    return get_available_reports(current_user.id)


def get_report_html(req_data):
    units = req_data['units']
    constructor = ReportConstructor(current_user.id, req_data['user_id'])
    for unit in units:
        if unit == 'user_plan':
            constructor.add_user_plan()
        if unit == 'user_stats':
            constructor.add_user_stats()
        if unit == 'users_categs':
            constructor.add_users_categs()
        if unit == 'plans_stats':
            constructor.add_plans_stats()
        if unit == 'users_list':
            constructor.add_users_list()
        if unit == 'all_stats':
            constructor.add_all_stats()
    return constructor.get_html()


def get_report_pdf(html):
    import random
    filename = ''
    for i in range(15):
        filename = filename + str(random.choice("0123456789ABCDEF"))
    filename = filename + '.pdf'
    actual_filename = 'app/static/generated_reports/' + filename
    pdfkit.from_string(html, actual_filename)
    url = url_for('static', filename=f'generated_reports/{filename}')
    return url
