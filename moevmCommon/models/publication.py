# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

TYPE_PUBLICATION_CHOICES = (
    ('g', 'Методическое указание'),
    ('b', 'Книга'),
    ('j', 'Статья в журнале'),
    ('s', 'Конспект лекции'),
    ('c', 'Сборник трудов')
)
reIter = (
    ('d', 'Одноразовый'),
    ('r', 'Повторяющийся')
)
class Publication(models.Model):
    name = models.CharField(max_length=250)

    user = models.ForeignKey(
        UserProfile,
        null=True
    )
    volume = models.CharField(
        max_length=100,
        null=True
    )
    publishingHouseName = models.CharField(
        max_length=100,
        null=True
    )
    publicationType = models.CharField(
        max_length=100,
        choices=TYPE_PUBLICATION_CHOICES,
        null=True
    )
    reiteration = models.CharField(
        choices=reIter,
        max_length=100,
        null=True
    )
    number = models.CharField(
        max_length=100,
        null=True
    )
    place = models.CharField(
        max_length=100,
        null=True
    )
    date = models.DateField(
        null=True
    )
    unitVolume = models.CharField(
        max_length=100,
        null=True
    )
    edition = models.CharField(
        max_length=100,
        null=True
    )
    type = models.CharField(
        max_length=100,
        null=True
    )
    isbn = models.CharField(
        max_length=100,
        null=True
    )
    editor = models.CharField(
        max_length=100,
        null=True
    )
    year = models.CharField(
        max_length=4,
        null=False
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
            year=params.get('year')
        )
        publication.save()
        return publication
    def __str__(self):
        return self.publicationType + ' ' + self.name + ' ' + self.isbn
