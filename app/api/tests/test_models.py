import unittest

from faker import Faker
from app.api.models import *
from models.default_model import DefaultModel


class ModelsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_model_classes(self):
        model_classes = get_model_classes()
        for model_class in model_classes:
            self.assertIsInstance(model_class, type(DefaultModel))

    def test_get_model_names(self):
        self.assertGreaterEqual(len(get_model_names()), 1)

    def test_get_models(self):
        models = get_models()
        self.assertGreaterEqual(len(models), 1)
        for model in models:
            self.assertIsNotNone(model['text'])
            self.assertIsNotNone(model['name'])
            self.assertIsNotNone(model['fields'])
            self.assertGreaterEqual(len(model['fields']), 1)

    def test_get_by_name(self):
        models = get_models()
        name = models[0]['name']
        self.assertIsInstance(get_model_class_by_name(name), type(DefaultModel))
        self.assertIsNotNone(get_model_info_by_name(name))
