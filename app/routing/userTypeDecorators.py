"""
==================
Декораторы доступа
==================
Несмотря на то, что ссылки на недоступные страницы вроде логов сервера скрыты от части пользователей, к ним могут
получить доступ все пользователи, просто введя нужный адрес. Данные декораторы же запрещают некоторым пользователям
проходить по определённым маршрутам или отправлять определённые запросы
"""
from functools import wraps
from flask_login import current_user
from app.api.users import get_user_type
import logging


def make_type_check_decorator(check_function):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def do_return(*_args, **_kwargs):
                from app.routing.routes import index
                logging.warning(f'Not enough authority to get to {func.__name__} ')
                return index(*_args, **_kwargs)
            if current_user.is_authenticated:
                if check_function():
                    return func(*args, **kwargs)
                else:
                    return do_return(*args, **kwargs)
            else:
                return do_return(*args, **kwargs)

        return wrapper
    return decorator


admin_required = make_type_check_decorator(lambda: get_user_type(current_user.id) == 'Администратор')
manager_required = make_type_check_decorator(lambda: get_user_type(current_user.id) != 'Преподаватель')
