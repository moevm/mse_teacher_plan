from datetime import datetime as dt

from flask import render_template
from flask_login import current_user

from app.api.plans import get_plans_stat, get_converted_user_plans
from app.api.users import count_users, count_user_categs, get_user_and_profile_list, get_profile_by_user_id


def get_current_profile():
    return get_profile_by_user_id(current_user.id)


def get_report_info(type_of_report):
    prof = get_current_profile()
    info = {
        'time': dt.now().strftime('%H:%M:%S'),
        'date': dt.now().strftime('%Y-%m-%d'),
        'creator': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic,
        'type': type_of_report
    }
    return info


def get_available_report_types():
    user = get_current_profile()
    res = [{
        'text': 'Статистика по пользователю',
        'name': 'user_stats'
    }]
    if user.type != 'Преподаватель':
        res.append({
            'text': 'Статистика по кафедре',
            'name': 'all_stats'
        })
    return res


def get_stat_report_template():
    info = get_report_info('Статистика по кафедре')
    plans_stat, total_plans = get_plans_stat()
    table_stats = [
        {
            'name': 'Общее количество пользователей',
            'value': count_users()
        },
        {
            'name': 'Общее количество планов',
            'value': total_plans
        }
    ]
    user_categs = count_user_categs()
    users_list = get_user_and_profile_list()
    users = [user['profile'] for user in users_list]
    return render_template('reports/statistic.html', info=info, stats=table_stats, plans=plans_stat,
                           user_categs=user_categs, users=users)


def get_user_stat_report_template(user_id):
    info = get_report_info('Статистика пользователя')
    if not user_id:
        user_id = current_user.id
    prof = get_profile_by_user_id(user_id)
    plans_stat, total_plans = get_plans_stat(user_id)
    plans_list = get_converted_user_plans(user_id)
    table_stats = [{
        'name': 'Пользователь',
        'value': prof.last_name + ' ' + prof.first_name + ' ' + prof.patronymic
    },
        {
            'name': 'Общее количество планов',
            'value': total_plans
        }
    ]
    return render_template('reports/user_stats.html', info=info, stats=table_stats, plans=plans_stat,
                           plans_list=plans_list)


def get_report_html(req_data):
    if req_data['type'] == 'all_stats':
        return get_stat_report_template()
    if req_data['type'] == 'user_stats':
        if req_data['user_id'] == 'All':
            req_data['user_id'] = None
        return get_user_stat_report_template(req_data['user_id'])
    return 'TODO?'
