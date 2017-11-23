#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile


TYPE_PUBLICATION_CHOICES = (
  ('guidelines', 'Методическое указание'),
  ('book', 'Книга'),
  ('journal', 'Статья в журнале'),
  ('compilation', 'Конспект лекции/сборник докладов'),
  ('collection ', 'Сборник трудов')
)

reIter = (
  ('disposable', 'Одноразовый'),
  ('repeating', 'Повторяющийся')
)


class Publication(models.Model):

  name = models.CharField(max_length=250)

  user = models.ForeignKey(
    UserProfile,
    null=True
  )

  # объем
  volume = models.CharField(
    "Объем",
    max_length="100",
    null=True
  )

  # название издательства
  publishingHouseName = models.CharField(
    "Название издательства",
    max_length="100",
    null=True
  )

  publicationType = models.CharField(
    "Тип публикации",
    max_length="100",
    choices=TYPE_PUBLICATION_CHOICES,
    default="book",
    null = True
  )

  # вид повторения сборника
  reiteration = models.CharField(
    "Вид повторения сборника",
    choices=reIter,
    max_length="100",
    default="disposable",
    null = True
    )

  # номер издания
  number = models.CharField(
    "Номер издания",
    max_length="100",
    null=True
  )

  # место издания
  place = models.CharField(
    "Место издания",
    max_length="100",
    null=True
  )

  # дата издания
  date = models.DateField(
    "Дата издания",
    null=True
  )

  # единицы объема
  unitVolume = models.CharField(
    "Единицы объёма",
    max_length="100",
    null = True
  )
  # тираж
  edition = models.CharField(
    "Тираж",
    max_length="100",
    null=True
  )

  # вид методического издания / книги
  type = models.CharField(
    "Вид",
    max_length="100",
    null=True
  )

  # ISBN
  isbn = models.CharField(
    "ISBN",
    max_length="100",
    null=True
  )

  # редактор сборника
  editor = models.CharField(
    "Редактор сборника",
    max_length="100",
    null=True
  )

  @staticmethod
  def create(**params):
    publication = Publication.objects.create(
      user=params.get('user'),
      name=params.get('name'),
      volume=params.get('volume'),
      publishingHouseName=params.get('publishingHouseName'),
      publicationType=params.get('publicationType'),
      reiteration=params.get('reiteration'),
      number=params.get('number'),
      place=params.get('place'),
      date=params.get('date'),
      unitVolume=params.get('unitVolume'),
      edition=params.get('edition'),
      type=params.get('type'),
      isbn=params.get('isbn'),
      editor=params.get('editor'),
    )

    publication.save()

    return publication

  def __str__(self):
    return self.publicationType + ' ' + self.name + ' ' + self.isbn