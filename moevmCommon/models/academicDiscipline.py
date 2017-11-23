#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile
#
# class AcademicDiscipline(models.Model):
#   name = models.CharField(max_length=150)
#
#   @staticmethod
#   def create(**params):
#     academicDiscipline = AcademicDiscipline.objects.create(
#       name=params.get('name'),
#     )
#     academicDiscipline.save()
#
#     return academicDiscipline
#
#   def __str__(self):
#     return self.name


class AcademicDisciplineOfTeacher(models.Model):
  user = models.ForeignKey(
    UserProfile,
    null=True
  )
  disc = models.CharField(
    max_length=40,
    null=True,
  )
  #Вид занятия
  type = models.CharField(
    max_length=40,
    null=True,
  )
  characterUpdate = models.CharField(
    max_length=250,
    null=True,
  )
  completeMark = models.CharField(
    max_length=250,
    null=True,
  )

  @staticmethod
  def create(**params):
    academicDisciplineOfTeacher = AcademicDisciplineOfTeacher.objects.create(
      user=params.get('user'),
      disc=params.get('disc'),
      type=params.get('type'),
      characterUpdate=params.get('characterUpdate'),
      completeMark=params.get('completeMark'),
    )
    academicDisciplineOfTeacher.save()

    return academicDisciplineOfTeacher

  def __str__(self):
    return self.disc + ' ' + self.type