# coding=utf-8
from mongoengine.document import Document
from mongoengine.fields import StringField
from werkzeug.security import generate_password_hash, check_password_hash

from models.plans.default_model import default_string_params


class Token(Document):
    """Модель токена.
    Содержимое токена неизвестно, известен только хэш.
    Токены используются для регистрации пользователей выше преподавателя
    """
    type = StringField(**default_string_params)
    token_hash = StringField(**default_string_params)

    def set_token(self, token):
        self.token_hash = generate_password_hash(token)

    def check_token(self, token):
        return check_password_hash(self.token_hash, token)

    meta = {
        'collection': 'Tokens'
    }
