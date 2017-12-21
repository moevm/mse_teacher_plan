# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

EVENT_TYPE_CHOISES = (
    ('k', 'Конкурс'),
    ('v', 'Выставка'),
    ('с', 'Конференция'),
    ('q', 'Семинар')
)
class ScientificEvent(models.Model):
    user = models.ForeignKey(
        UserProfile,
        null=True
    )
    event_name = models.CharField(max_length=255)
    level = models.CharField(
        max_length=20,
        null=True
    )
    date = models.DateField(
        null=True
    )
    place = models.CharField(
        max_length=100,
        null=True
    )
    type = models.CharField(
        max_length=1,
        choices=EVENT_TYPE_CHOISES
    )
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        scientificEvent = ScientificEvent.objects.create(
            user=params.get('user'),
            event_name=params.get('event_name'),
            level=params.get('level'),
            date=params.get('date'),
            place=params.get('place'),
            type=params.get('type'),
            year=params.get('year')
        )
        scientificEvent.save()
        return scientificEvent
    def __str__(self):
        return self.type + " " + self.level + " " + self.event_name
