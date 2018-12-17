import unittest

from app.api.users import register_fake_user, get_user_by_login, delete_user
from faker import Faker

from app.api.reports import *
from app.models.fake.profile import ProfileProvider


class ReportsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_all_reports(self):
        reports = get_all_reports()
        self.assertGreater(len(reports), 1)

    def test_available_reports(self):
        fake = Faker()
        fake.add_provider(ProfileProvider)
        fake_user = register_fake_user(fake)
        fake_user_id = get_user_by_login(fake_user['login']).id
        available_reports = get_available_reports(fake_user_id)
        self.assertIsNotNone(available_reports)
        delete_user(fake_user_id)
