# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class AcademicDisciplineOfTeacher(models.Model):
    user = models.ForeignKey(
        UserProfile,
        null=True
    )
    disc = models.CharField(
        max_length=40,
        null=True,
    )
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
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        academicDisciplineOfTeacher = AcademicDisciplineOfTeacher.objects.create(
            user=params.get('user'),
            disc=params.get('disc'),
            type=params.get('type'),
            characterUpdate=params.get('characterUpdate'),
            completeMark=params.get('completeMark'),
            year=params.get('year')
        )
        academicDisciplineOfTeacher.save()
        return academicDisciplineOfTeacher
    def __str__(self):
        return self.disc + ' ' + self.type
