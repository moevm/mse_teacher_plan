# coding=utf-8
from mongoengine.document import Document
from mongoengine.fields import StringField
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.plans.default_model import default_string_params


class Token(Document):
    """Модель токена.
    Содержимое токена неизвестно, известен только хэш.
    Токены используются для регистрации пользователей выше преподавателя
    """
    type = StringField(**default_string_params)
    token_hash = StringField(**default_string_params)

    def set_token_key(self, token):
        """
        Устанавливает ключ для токена. Так как хранится только хэщ, восстановить ключ
        очень сложно
        :param token: Любая строка
        """
        self.token_hash = generate_password_hash(token)

    def check_token(self, token):
        """
        Проверяет, совпадает ли хэш-сумма поданного на вход ключа с установленной в данном
        :param token: Строка-ключ
        :return: True, если совпадает
        """
        return check_password_hash(self.token_hash, token)

    meta = {
        'collection': 'Tokens'
    }
