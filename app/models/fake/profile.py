from faker import Faker
from faker.providers import BaseProvider
from app.models.profile import user_type_choices, user_academic_status_choices
import random


class ProfileProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.fake = Faker()

    def first_name(self):
        return self.fake.first_name()

    def last_name(self):
        return self.fake.last_name()

    def patronymic(self):
        return self.fake.first_name()

    def type(self):
        return random.choice(user_type_choices)

    def birth_date(self):
        return str(self.fake.date())

    def github_id(self):
        return self.fake.random_number(10)

    def stepic_id(self):
        return self.fake.random_number(10)

    def election_date(self):
        return str(self.fake.date())

    def contract_date(self):
        return str(self.fake.date())

    def academic_status(self):
        return random.choice(user_academic_status_choices)

    def year_of_academic_status(self):
        return self.fake.year()

    def moevm_profile(self):
        return {
            'last_name': self.last_name(),
            'first_name': self.first_name(),
            'patronymic': self.patronymic(),
            'type': self.type(),
            'birth_date': self.birth_date(),
            'github_id': self.github_id(),
            'stepic_id': self.stepic_id(),
            'election_date': self.election_date(),
            'contract_date': self.contract_date(),
            'academic_status': self.academic_status(),
            'year_of_academic_status': self.year_of_academic_status()
        }
