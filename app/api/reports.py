"""
=====================
API генерации отчётов
=====================
Информация о типах доступных отчётов, также, как и о моделях, хранится в БД.
"""

from typing import Dict, List
from app.api.users import get_user_by_id, get_profile_by_user_id
from app.models.model import DocId
from app.models.report import Report


def get_all_reports()->List[Dict[str, str]]:
    """
    Получить информацию о всех отчётах
    Структура возвращаемого объекта:
    [
        {
            'name' - имя
            'text' - отображаемый текст
            'min_auth' - минимальный уровень допуска
        }
    ]
    """
    reports = Report.objects()
    res = []
    for report in reports:
        res.append({
            "name": report.name,
            "text": report.text,
            "min_auth": report.min_auth
        })
    return res


def get_available_reports(user_id: DocId)->List[Dict[str, str]]:
    """
    Получение информации об отчётах, доступных данному пользователю.
    Структура return такая же, как и в
    get_all_reports()
    :param user_id: Id пользователя
    """
    def compare_categories(category1: str, category2: str)->int:
        categories = ['Преподаватель', 'Менеджер', 'Администратор']
        res1 = categories.index(category1)
        res2 = categories.index(category2)
        return res1 - res2

    profile = get_profile_by_user_id(user_id)
    reports = get_all_reports()
    user_type = profile.type
    res = []
    for report in reports:
        if compare_categories(user_type, report['min_auth']) >= 0:
            res.append(report)
    return res
