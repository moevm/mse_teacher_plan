# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class Qualification(models.Model):
    user = models.ForeignKey(UserProfile)
    courseName = models.CharField(max_length=250)
    discipline = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    startDate = models.DateField(null=True)
    finishDate = models.DateField(null=True)
    organisation = models.CharField(
        max_length=250,
        null=True
    )
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        qualification = Qualification.objects.create(
            user=params.get('user'),
            courseName=params.get('courseName'),
            discipline=params.get('discipline'),
            authors=params.get('authors'),
            startDate=params.get('startDate'),
            finishDate=params.get('finishDate'),
            organisation=params.get('organisation'),
            year=params.get('year')
        )
        qualification.save()
        return qualification
    def __str__(self):
        return self.courseName + " " + self.organisation
