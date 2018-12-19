# coding=utf-8
"""
=========================
API для работы с токенами
=========================
Токен - шифрованный ключ, необходимый для авторизации какого-либо действия. Хранится лишь хэш токена,
чтобы нельзя было получить токен, просто зайдя в БД.

"""
import random
from typing import List, Dict

from app.models.model import DocId

from app.models.token import Token

manager_tokens = [{
    'text': 'Регистрация менеджера',
    'name': 'REG_MNG'
}]
admin_tokens = [{
    'text': 'Регистрация администратора',
    'name': 'REG_ADM'
}]


def get_new_token(type: str)->str:
    """
    Генерирует новый токен и сохраняет в БД
    :return: Строка с ключом токена
    """
    token_key = ""
    for i in range(15):
        token_key = token_key + str(random.choice("0123456789ABCDEF"))
    token = Token()
    token.set_token_key(token_key)
    token.type = type
    token.save()
    return token_key


def use_token(token_key: str, expected_token_type: str) -> bool:
    """
    Использует токен. Использованный токен удаляется
    :param token_key: Ключ токена
    :param expected_token_type: Ожидаемый тип токена
    :return: True, если использован успешно, и False, если нет
    """
    token = check_token(token_key, expected_token_type)
    if token:
        activate_token(token)
        return True
    return False


def check_token(token_key: str, expected_token_type: str):
    """
    Проверяет правильность токена и вовзращает объект токена.
    Полезно, если между проверкой наличия и использования может быть
    необходимость прервать операцию
    :param token_key: Ключ токена
    :param expected_token_type: Ожидаемый тип токена
    :return: Объект токена
    """
    for token in Token.objects:
        if token.check_token(token_key) and token.type == expected_token_type:
            return token


def activate_token(token):
    """
    Удаляет токен. Если объект токена пустой, ничего не делает!
    :param token: Объект токена
    """
    if token:
        token.delete()


def get_available_token_types(id: DocId)->List[Dict[str, str]]:
    """
    Выдает список токенов, которые может выдать пользователь
    :param id: Id пользователя
    :return: Список строк
    """
    from app.api.users import get_user_type
    type = get_user_type(id)
    res = []
    if type != 'Преподаватель':
        res.extend(manager_tokens)
    if type == 'Администратор':
        res.extend(admin_tokens)
    return res


def check_token_availability(id: DocId, type: str)->bool:
    """
    Проверяет, досупен ли данному пользователю данный тип токенов
    :param id: Id пользователя
    :param type: Тип
    :return: True или False
    """
    types = get_available_token_types(id)
    for available_type in types:
        if available_type['name'] == type:
            return True
    return False
