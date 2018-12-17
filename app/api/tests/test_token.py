import unittest

from app.api.users import register_fake_user, get_user_by_login, get_profile_by_user_id, delete_user, register_user
from faker import Faker

from app.api.tokens import *
from app.models.fake.profile import ProfileProvider


class TokenTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_token(self):
        token_str = get_new_token('TEST_TYPE')
        self.assertGreater(len(token_str), 1)
        self.assertFalse(use_token(token_str, 'LOL'))
        self.assertFalse(use_token('LOL', 'TEST_TYPE'))
        self.assertTrue(use_token(token_str, 'TEST_TYPE'))
        self.assertFalse(use_token(token_str, 'TEST_TYPE'))

    def test_get_available_tokens(self):
        fake = Faker()
        fake.add_provider(ProfileProvider)
        fake_user = register_fake_user(fake)
        fake_user_id = get_user_by_login(fake_user['login']).id
        fake_user_profile = get_profile_by_user_id(fake_user_id)
        fake_user_profile.type = 'Преподаватель'
        fake_user_profile.save()
        prep_types = get_available_token_types(fake_user_id)
        self.assertIsNotNone(prep_types)

        fake_user_profile.type = 'Менеджер'
        fake_user_profile.save()
        mng_types = get_available_token_types(fake_user_id)
        self.assertGreaterEqual(len(mng_types), len(prep_types))

        fake_user_profile.type = 'Администратор'
        fake_user_profile.save()
        adm_types = get_available_token_types(fake_user_id)
        self.assertGreaterEqual(len(adm_types), len(mng_types))
        if len(adm_types) > 0:
            self.assertTrue(check_token_availability(fake_user_id, adm_types[0]['name']))

        delete_user(fake_user_id)

    def test_register_user(self):
        fake = Faker()
        fake.add_provider(ProfileProvider)
        token_adm = get_new_token('REG_ADM')
        fake_user = fake.moevm_profile()
        fake_user['login'] = fake.user_name()
        fake_user['password'] = fake.password()
        fake_user['token'] = token_adm
        fake_user['type'] = 'Администратор'
        user = register_user(fake_user)
        self.assertIsNotNone(user)
        self.assertIsNone(check_token(token_adm, 'REG_ADM'))
        delete_user(user.id)

