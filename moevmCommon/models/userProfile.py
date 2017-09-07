#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

PERSON_TYPE_CHOICES = (
    ('s', 'Студент'),
    ('h', 'Староста'),
    ('t', 'Преподаватель'),
    ('a', 'Администратор'),
)
ACADEMIC_STATUS_CHOICES  = (
  ('a','Ассистент'),
  ('s','Старший преподаватель'),
  ('d','Доцент'),
  ('p','Профессор'),
)

ACADEMIC_DEGREE_CHOICES = (
  ('n','Без степени'),
  ('t','Кандидат наук'),
  ('d','Доктор наук'),
)

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  patronymic = models.CharField(
    max_length=30,
    null=True,
  )
  birth_date = models.DateField(
    null=True,
  )
  study_group = models.CharField(
    max_length=5,
    null=True,
  )
  github_id = models.CharField(
    max_length=100,
    null=True,
  )
  stepic_id = models.CharField(
    max_length=100,
    null=True,
  )

  type = models.CharField(
    max_length=2,
    choices=PERSON_TYPE_CHOICES,
    default='s',
  )

  # Дата текущего избрания или зачисления на преподавательскую должность
  election_date = models.DateField(null=True)

  # Должность
  position = models.CharField(max_length=40, null=True)

  # Срок окончания трудового договора
  contract_date = models.DateField(null=True)  # Возможн поменяю

  # Ученая степень
  academic_degree = models.CharField(
    max_length=1,
    choices=ACADEMIC_DEGREE_CHOICES,
    null=True
  )

  # Год присвоения ученой степени
  year_of_academic_degree = models.DateField(null=True)

  # Учебное звание
  academic_status = models.CharField(
    max_length=1,
    choices=ACADEMIC_STATUS_CHOICES,
    null=True)
  year_of_academic_status = models.DateField(null=True)

  @property
  def first_name(self):
    return self.user.first_name

  @property
  def last_name(self):
    return self.user.last_name

  @property
  def login(self):
    return self.user.username

  @property
  def password(self):
    return self.user.password

  @property
  def email(self):
    return self.user.email

  @staticmethod
  def create(login, password, email, **params):
    user = User.objects.create_user(login, password, email)
    user.first_name = params.get('first_name')
    user.last_name = params.get('last_name')
    user.save()

    user_profile = UserProfile.objects.create(
      user=user,
      patronymic=params.get('patronymic'),
      birth_date=params.get('birth_date'),
      study_group=params.get('study_group'),
      github_id=params.get('github_id'),
      stepic_id=params.get('stepic_id'),
      type=params.get('type', 's'),
      election_date=params.get('election_date'),
      position=params.get('position'),
      contract_date=params.get('contract_date'),
      academic_degree=params.get('academic_degree'),
      year_of_academic_degree=params.get('year_of_academic_degree'),
      academic_status=params.get('academic_status'),
      year_of_academic_status=params.get('year_of_academic_status')
    )

    user_profile.save()

    return user_profile

  @staticmethod
  def create_of_user(**params):
    user_profile = UserProfile.objects.create(
      user=params.get('user'),
      patronymic=params.get('patronymic'),
      birth_date=params.get('birth_date'),
      study_group=params.get('study_group'),
      github_id=params.get('github_id'),
      stepic_id=params.get('stepic_id'),
      type=params.get('type', 's'),
      election_date=params.get('election_date'),
      position=params.get('position'),
      contract_date=params.get('contract_date'),
      academic_degree=params.get('academic_degree'),
      year_of_academic_degree=params.get('year_of_academic_degree'),
      academic_status=params.get('academic_status'),
      year_of_academic_status=params.get('year_of_academic_status')
    )

    return user_profile

  def __str__(self):
    return self.first_name + ' ' + self.last_name + ' ' + self.patronymic

  class Meta:
    db_table = 'userprofiles'