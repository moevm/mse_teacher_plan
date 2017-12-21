#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from moevmCommon.models.userProfile import *
from moevmCommon.models.academicDiscipline import *
from moevmCommon.models.nir import *
from moevmCommon.models.publication import *
from moevmCommon.models.scientificEvent import *
from moevmCommon.models.books import *
from moevmCommon.models.qualification import *
from moevmCommon.models.other import *

admin.site.register(UserProfile)
# admin.site.register(AcademicDiscipline)
admin.site.register(AcademicDisciplineOfTeacher)
admin.site.register(NIR)
admin.site.register(ScientificEvent)
# admin.site.register(Participation)
admin.site.register(Publication)
admin.site.register(Book)
admin.site.register(Qualification)
admin.site.register(Other)