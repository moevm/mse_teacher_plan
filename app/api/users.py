from typing import Union, List

import mongoengine

from app.api.convert import convert_mongo_model, ConvertedDocument
from app.models.profile import Profile
from app.models.user import User
from models.model import DocId


# Получить профиль, привязанный к пользователю
def get_profile_by_user_id(id: DocId) -> Union[Profile, None]:
    for c_user in Profile.objects(user=id):
        return c_user
    return None


def get_user_by_login(login: str) -> Union[User, None]:
    try:
        found_user = User.objects.get(login=login)
    except User.DoesNotExist:
        return None
    return found_user


# Найти пользователя по id
def get_user_by_id(id: DocId) -> Union[User, None]:
    try:
        found_user = User.objects.get(id=id)
    except User.DoesNotExist:
        return None
    return found_user


# Получить тип пользователя
def get_user_type(id: DocId) -> Union[str, None]:
    profile = get_profile_by_user_id(id)
    if profile:
        return profile.type
    return None


# Получить список профилей, к чьим планам данный имеет доступ
def get_available_profiles(user: User) -> List[Profile]:
    profile = get_profile_by_user_id(user.id)
    res = []
    if profile.type == 'Администратор' or profile.type == 'Менеджер':
        for prof in Profile.objects():
            res.append(prof)
    else:
        res = [profile]
    return res


# Получить список пользователей, к чьим планам данный имеет доступ
def get_available_users(user: User) -> List[User]:
    profile = get_profile_by_user_id(user.id)
    res = []
    if profile.type == 'Администратор' or profile.type == 'Менеджер':
        for us in User.objects():
            res.append(us)
    else:
        res = [user]
    return res


# Проверить логин и пароль
def check_user_auth(user_data) -> Union[User, None]:
    try:
        found_user = User.objects.get(login=user_data['login'])
    except User.DoesNotExist:
        return None
    if found_user is not None and found_user.check_password(user_data['password']):
        return found_user
    else:
        return None


# Вернуть параметры формы для регистрации
def get_registration_form() -> ConvertedDocument:
    def f(text, name, type, opts=None, value=''):
        if opts is None:
            opts = []
        return {'text': text, 'name': name, 'type': type, 'opts': opts, 'value': value}
    form = [
                  f('Логин', 'login', 'text'),
                  f('Пароль', 'password', 'text')
              ] + convert_mongo_model(Profile)
    return form


# Зарегистровать пользователя по возвращенной форме
def register_user(registration_data) -> User:
    registration_data = dict(registration_data)
    user = User(
        login=registration_data['login']
    )
    user.set_password(registration_data['password'])
    del registration_data['login']
    del registration_data['password']
    profile = Profile(user=user, **registration_data)
    user.save()
    try:
        profile.save()
    except:
        user.delete()
        raise
    return user


# Обновление профиля. Обязательно поле 'id' для объекта Profile
def update_profile(profile_data):
    profile_data = dict(profile_data)
    if 'user' in profile_data:
        del profile_data['user']
    profile = Profile.objects.get(id=profile_data['id'])
    del profile_data['id']
    for entry in profile_data:
        profile[entry] = profile_data[entry]
    profile.save()


# Удаление пользователя
def delete_user(id: DocId):
    try:
        found_user = User.objects.get(id=id)
        profile = get_profile_by_user_id(id)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return None
    found_user.delete()
    profile.delete()
