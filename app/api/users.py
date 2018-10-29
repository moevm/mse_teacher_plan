from app.api.convert import convert_mongo_model
from app.models.profile import Profile
from app.models.user import User


# Получить профиль, привязанный к пользователю
def get_profile_by_user_id(id):
    for c_user in Profile.objects(user=id):
        return c_user
    return None


# Получить список пользователей, к чьим планам данный имеет доступ
def get_available_users(user):  # TODO
    res = [get_profile_by_user_id(user.id)]
    return res


# Проверить логин и пароль
def check_user_auth(user_data):
    try:
        found_user = User.objects.get(login=user_data['login'])
    except User.DoesNotExist:
        return None
    if found_user is not None and found_user.check_password(user_data['password']):
        return found_user
    else:
        return None


# Вернуть параметры формы для регистрации
def get_registration_form():
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
def register_user(registration_data):
    user = User(
        login=registration_data['login']
    )
    user.set_password(registration_data['password'])
    del registration_data['login']
    del registration_data['password']
    profile = Profile(user=user, **registration_data)
    user.save()
    profile.save()


# Обновление профиля. Обязательно поле 'id'
def update_profile(profile_data):
    if 'user' in profile_data:
        del profile_data['user']
    profile = Profile.objects.get(id=profile_data['id'])
    del profile_data['id']
    for entry in profile_data:
        profile[entry] = profile_data[entry]
    profile.save()