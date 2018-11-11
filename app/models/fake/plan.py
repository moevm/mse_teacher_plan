import random

from faker import Faker


def generate_fake_by_converted_model(model):
    res = {}
    fake = Faker()
    for field in model:
        if field['text'] != '%NO_VERBOSE_NAME%':
            if len(field['opts']) != 0:
                res[field['name']] = random.choice(field['opts'])
            elif field['type'] == 'text':
                res[field['name']] = fake.text(25)[:-1]
            elif field['type'] == 'number':
                res[field['name']] = fake.year()
            elif field['type'] == 'date':
                res[field['name']] = fake.date()
    res['year'] = random.choice([str(i) for i in range(2014, 2024)])
    return res
