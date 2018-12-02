from typing import Union, List, Dict

from app.api.convert import ConvertedDocument, convert_mongo_model, convert_mongo_document
from app.models.profile import Profile
from app.models.user import User
from app.models.model import DocId


def register_multiple_fake_users(user_number: int, plans_number: int):
    from faker import Faker
    fake = Faker()
    from app.models.fake.profile import ProfileProvider
    fake.add_provider(ProfileProvider)
    for i in range(user_number):
        register_fake_user(fake, plans_number)


def register_fake_user(fake, plans_number=0):
    fake_user = fake.moevm_profile()
    fake_user['login'] = fake.user_name()
    fake_user['password'] = fake.password()
    user = register_user(fake_user)
    if plans_number > 0:
        from app.api.plans import new_multiple_fake_plans
        new_multiple_fake_plans(user.id, plans_number)
    return fake_user


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


# Сменить пароль
def change_password(id:DocId, old_password, new_password) -> bool:
    user = get_user_by_id(id)
    if not user:
        return False
    return user.change_password(old_password, new_password)


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
    from app.api.plans import delete_user_plans
    delete_user_plans(id)
    found_user.delete()
    profile.delete()


# Получить список пользователей
def get_user_and_profile_list():
    res = []
    for user in User.objects():
        profile = get_profile_by_user_id(user.id)
        res.append({
            'user': convert_mongo_document(user),
            'profile': convert_mongo_document(profile)
        })
    return res


# Подсчитать пользователей
def count_users():
    return len(get_user_and_profile_list())


# Подсчитать количество пользователей в категориях
def count_user_categs()-> List[Dict[str, Union[str, Dict[str, int]]]]:
    def get_opts(converted_doc: ConvertedDocument)\
            ->List[Dict[str, Union[str, int, List[str]]]]:
        fields_with_opts = []
        for field in converted_doc:
            if field['opts']:
                fields_with_opts.append(field)
        return fields_with_opts

    def get_opt_type(converted_doc: ConvertedDocument, req_field: Dict[str, str])->str:
        for field in converted_doc:
            if field['name'] == req_field['name']:
                return field['value']

    def count_opts(data: List[ConvertedDocument], opt_fields: List[Dict[str, str]])\
            ->List[Dict[str, Union[str, Dict[str, int]]]]:
        final_res = []
        for opt_field in opt_fields:
            res = {}
            for elem in data:
                elem_type = get_opt_type(elem, opt_field)
                if elem_type not in res:
                    res[elem_type] = 1
                else:
                    res[elem_type] = res[elem_type] + 1
            final_res.append({
                'name': opt_field['text'],
                'count': res
            })
        return final_res

    all = get_user_and_profile_list()
    first = all[0]
    # user_opts = get_opts(first['user'])
    profile_opts = get_opts(first['profile'])
    # users = [user['user'] for user in all]
    profiles = [user['profile'] for user in all]
    return count_opts(profiles, profile_opts)



