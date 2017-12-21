# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class Other(models.Model):
    user = models.ForeignKey(UserProfile)
    startDate = models.DateField(null=True)
    finishDate = models.DateField(null=True)
    kindOfWork = models.CharField(
        max_length=250,
        null=True
    )
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        other = Other.objects.create(
            user=params.get('user'),
            startDate=params.get('startDate'),
            finishDate=params.get('finishDate'),
            kindOfWork=params.get('kindOfWork'),
            year=params.get('year')
        )
        other.save()
        return other
    def __str__(self):
        return self.kindOfWork
