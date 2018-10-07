# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class Book(models.Model):
    user = models.ForeignKey(UserProfile)
    bookName = models.CharField(max_length=250)
    discipline = models.CharField(max_length=250)
    authors = models.CharField(max_length=250)
    date = models.CharField(max_length=4)
    organisation = models.CharField(
        max_length=250,
        null=True
    )
    cipher = models.CharField(
        max_length=100,
        null=True
    )
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        book = Book.objects.create(
            user=params.get('user'),
            authors=params.get('authors'),
            bookName=params.get('bookName'),
            discipline=params.get('discipline'),
            date=params.get('date'),
            organisation=params.get('organisation'),
            cipher=params.get('cipher'),
            year=params.get('year')
        )
        book.save()
        return book
    def __str__(self):
        return self.bookName + " " + self.organisation + " " + self.cipher
