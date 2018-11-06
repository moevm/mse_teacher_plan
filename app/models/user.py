from flask_login import UserMixin

from app import login
from mongoengine.document import Document
from mongoengine.fields import StringField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
default_params = {'required': True}
default_string_params = {**default_params, 'max_length': 250}


class User(Document, UserMixin):
    login = StringField(**default_params, unique=True)
    password_hash = StringField(**default_params)
    authenticated = BooleanField(default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):  # All users are active
        return True

    def get_id(self):
        return self.login

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    meta = {'collection': 'Users'}


@login.user_loader
def load_user(id):
    for user in User.objects(login=id):
        return user
    return None