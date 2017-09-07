#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class NIR(models.Model):
  user = models.ForeignKey(UserProfile)
  workName = models.CharField(max_length=250)
  startDate = models.DateField(null=True)
  finishDate = models.DateField(null=True)
  role = models.CharField(
    max_length=100,
    null=True
  )
  organisation = models.CharField(
    max_length=250,
    null=True
  )
  # Шифр
  cipher = models.CharField(
    "Шифр",
    max_length="100",
    null=True
  )

  @staticmethod
  def create(**params):
    nir = NIR.objects.create(
      user=params.get('user'),
      startDate=params.get('startDate'),
      finishDate = params.get('finishDate'),
      role = params.get('role'),
      organisation = params.get('organisation'),
      cipher = params.get('cipher'),
    )

    nir.save()

    return nir

  def __str__(self):
    return self.workName + " " + self.organisation + " " + self.cipher