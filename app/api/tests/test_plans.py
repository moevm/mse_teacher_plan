import unittest

from faker import Faker

from app.api.models import get_models
from app.api.users import register_user, delete_user, get_user_by_login
from app.api.plans import *
from app.models.default_model import DefaultModel
from app.models.fake.profile import ProfileProvider


class PlansTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.fake = Faker()
        cls.fake.add_provider(ProfileProvider)
        cls.fake_user = cls.fake.moevm_profile()
        cls.fake_user['login'] = cls.fake.user_name()
        cls.fake_user['password'] = cls.fake.password()
        cls.user = register_user(cls.fake_user)
        plan_type = get_models()[0]['name']
        cls.fake_plan = new_fake_plan(cls.user.id, plan_type)

    def test_modify(self):
        save_plan(self.fake_plan.id, {
            'year': '2018'
        })

    def test_get_document(self):
        document = get_plan_document(self.fake_plan.id)
        self.assertIsNotNone(document)

    def test_get_plan(self):
        plan = get_plan(self.fake_plan.id)
        self.assertGreaterEqual(len(plan), 1)

    def test_get_user_plans(self):
        plans = get_converted_user_plans(self.user.id, 0, 10000)
        self.assertEqual(plans[0]['plans'][0], get_plan(self.fake_plan.id))

    def test_get_all_plans(self):
        all_conv_plans = get_converted_user_plans()
        all_plans = get_user_plans()
        stats = get_plans_stat()
        conv_plan_cnt = 0
        for i in range(len(all_conv_plans)):
            plan_type = all_conv_plans[i]
            conv_plan_cnt = conv_plan_cnt + len(plan_type['plans'])
            self.assertEqual(len(plan_type['plans']), stats[i]['plans_num'])
        self.assertEqual(conv_plan_cnt, len(all_plans))

    def test_available_plans(self):
        plans = get_available_users(self.user)
        self.assertGreaterEqual(len(plans), 1)
        available_plans = get_converted_available_plans(self.user.id, 0, 10000)
        self.assertGreaterEqual(len(available_plans), 1)

    def test_multiple(self):
        new_multiple_fake_plans(self.user.id, 10)
        plans = get_user_plans(self.user.id)
        self.assertGreaterEqual(len(plans), 10)

    @classmethod
    def tearDownClass(cls):
        fake_user_id = get_user_by_login(cls.fake_user['login']).id
        delete_user(fake_user_id)
        delete_plan(cls.fake_plan.id)



