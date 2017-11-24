# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from moevmCommon.models.userProfile import UserProfile
from django.http import HttpResponseRedirect
import datetime
from moevmCommon.models.nir import NIR
from moevmCommon.models.publication import Publication
from moevmCommon.models.scientificEvent import ScientificEvent
from moevmCommon.models.academicDiscipline import AcademicDisciplineOfTeacher
from django.db import models
from django.contrib.auth.models import User
from django import forms

@login_required(login_url="/login")
def index(request):
    if list(UserProfile.objects.filter(user_id=request.user.id)) == []:
        user = User.objects.get(id=request.user.id)
        patronymic = ""
        type = "t"
        birth_date = "2017-01-01"
        github_id = ""
        stepic_id = ""
        election_date = "2017-01-01"
        contract_date = "2017-01-01"
        academic_status = "a"
        year_of_academic_status = "2017-01-01"
        academic_degree = "n"
        year_of_academic_degree = "2017-01-01"
        user.first_name = ""
        user.last_name = ""
        user.save()
        user_profile = UserProfile.objects.create(
            user=user,
            patronymic=patronymic,
            birth_date=birth_date,
            github_id=github_id,
            stepic_id=stepic_id,
            type=type,
            election_date=election_date,
            contract_date=contract_date,
            academic_degree=academic_degree,
            year_of_academic_degree=year_of_academic_degree,
            academic_status=academic_status,
            year_of_academic_status=year_of_academic_status)
        return render(request, 'profileNew.html')
    else:
        profile = UserProfile.objects.get(user_id=request.user.id)
        context = {
            'profile': profile,
            'user': request.user,
        }
        return render(request, 'index.html', context)

def loginTeacher(request):
    if request.method == 'POST':
        username = request.POST['loginField']
        password = request.POST['passwordField']
        print username
        print password
        user = auth.authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/loginwitherror')
        else:
            print "Некорректные данные: Логин {0}, Пароль {1}".format(username, password)
            return HttpResponseRedirect('/loginwitherror')
    return render(request, 'login.html')

def errorLoginTeacher(request):
    return render(request, 'login.html',{'error_message': 'Ошибка авторизации'})

@login_required(login_url="/login")
def logoutTeacher(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required(login_url="/login")
def makeNewPlan(request):

    return render(request, 'makeNewPlan.html')

def validate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@login_required(login_url="/login")
def makeNewPlanSaveNIR(request):
    profile = UserProfile.objects.get(user_id=request.user.id)

    iNir = 0

    workName = request.POST.get("workName")
    if workName != "": iNir+=1

    startDate = request.POST.get("startDate")
    if (startDate != "") and (validate(startDate)): iNir += 1

    role = request.POST.get("role")
    if role != "": iNir += 1

    organisation = request.POST.get("organisation")
    if organisation != "": iNir += 1

    cipher = request.POST.get("cipher")
    if cipher != "": iNir += 1

    finishDate = request.POST.get("finishDate")
    if (finishDate != "") and (validate(finishDate)): iNir += 1

    if iNir == 6:
        NIR.objects.create(
            user=profile,
            workName=workName,
            startDate=startDate,
            role=role,
            organisation=organisation,
            cipher=cipher,
            finishDate=finishDate)

    render(request, 'makeNewPlan.html')
    return HttpResponseRedirect('/makeNewPlan')

@login_required(login_url="/login")
def makeNewPlanSavePublication(request):
    profile = UserProfile.objects.get(user_id=request.user.id)

    iPubl = 0

    publicationType = request.POST.get("publicationType")
    if publicationType != "":
        if publicationType == u"Методическое указание":
            publicationType = 'guidelines'
            iPubl+=1
        if publicationType == u"Книга":
            publicationType = 'book'
            iPubl += 1
        if publicationType == u"Статья в журнале":
            publicationType = 'journal'
            iPubl += 1
        if publicationType == u"Конспект лекции/сборник докладов":
            publicationType = 'compilation'
            iPubl += 1
        if publicationType == u"Сборник трудов":
            publicationType = 'collection'
            iPubl += 1

    reiteration = request.POST.get("reiteration")
    if reiteration != "":
        if reiteration == u"Одноразовый":
            iPubl += 1
            publicationType = 'disposable'
        if reiteration == u"Повторяющийся":
            iPubl += 1
            publicationType = 'repeating'

    name = request.POST.get("name")
    if name != "": iPubl += 1

    unitVolume = request.POST.get("unitVolume")
    if unitVolume != "": iPubl += 1

    publishingHouseName = request.POST.get("publishingHouseName")
    if publishingHouseName != "": iPubl += 1

    number = request.POST.get("number")
    if number != "": iPubl += 1

    volume = request.POST.get("volume")
    if volume != "": iPubl += 1

    edition = request.POST.get("edition")
    if edition != "": iPubl += 1

    place = request.POST.get("place")
    if place != "": iPubl += 1

    editor = request.POST.get("editor")
    if editor != "": iPubl += 1

    date = request.POST.get("date")
    if date != "" and (validate(date)): iPubl += 1

    isbn = request.POST.get("isbn")
    if isbn != "": iPubl += 1

    type = request.POST.get("type")
    if type != "": iPubl += 1

    if iPubl == 13:
        Publication.objects.create(
            user=profile,
            name=name,
            volume=volume,
            publishingHouseName=publishingHouseName,
            publicationType=publicationType,
            reiteration=reiteration,
            number=number,
            place=place,
            date=date,
            unitVolume=unitVolume,
            edition=edition,
            type=type,
            isbn=isbn,
            editor=editor)

    render(request, 'makeNewPlan.html')
    return HttpResponseRedirect('/makeNewPlan')

@login_required(login_url="/login")
def makeNewPlanSaveScience(request):
    profile = UserProfile.objects.get(user_id=request.user.id)

    iSci = 0

    event_name = request.POST.get("event_name")
    if event_name != "": iSci+=1

    date = request.POST.get("date")
    if (date != "") and (validate(date)): iSci += 1

    level = request.POST.get("level")
    if level != "": iSci += 1

    place = request.POST.get("place")
    if place != "": iSci += 1

    type = request.POST.get("type")
    if type != "":
        if type == u"Конкурс":
            iSci += 1
            type = 'k'
        if type == u"Выставка":
            iSci+= 1
            type = 'v'
        if type == u"Конференция":
            iSci += 1
            type = 'c'
        if type == u"Семинар":
            iSci += 1
            type = 'q'

    if iSci == 5:
        ScientificEvent.objects.create(
            user=profile,
            event_name=event_name,
            level=level,
            date=date,
            place=place,
            type=type)

    render(request, 'makeNewPlan.html')
    return HttpResponseRedirect('/makeNewPlan')

@login_required(login_url="/login")
def makeNewPlanSaveDisc(request):
    userProf = request.POST.get("UserProfile")

    profile = UserProfile.objects.get(user_id=request.user.id)

    iDisc = 0

    characterUpdate = request.POST.get("characterUpdate")
    if characterUpdate != "": iDisc+=1

    disc = request.POST.get("disc")
    if disc != "": iDisc += 1

    type = request.POST.get("type")
    if type != "": iDisc += 1

    completeMark = request.POST.get("completeMark")
    if completeMark != "": iDisc += 1

    if iDisc == 4:
        AcademicDisciplineOfTeacher.objects.create(
            user=profile,
            disc=disc,
            type=type,
            characterUpdate=characterUpdate,
            completeMark=completeMark)

    render(request, 'makeNewPlan.html')
    return HttpResponseRedirect('/makeNewPlan')

@login_required(login_url="/login")
def profileOpen(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'profileOpen.html', context)

@login_required(login_url="/login")
def profileSave(request):
    profile = UserProfile.objects.get(user_id=request.user.id)

    lastName = request.POST.get("lastName")
    if lastName != "":
        profile.user.last_name = lastName

    firstName = request.POST.get("firstName")
    if firstName != "":
        profile.user.first_name = firstName

    patronymic = request.POST.get("patronymic")
    if patronymic != "":
        profile.patronymic = patronymic

    type = request.POST.get("type")
    if type != "":
        if type == u"Преподаватель": profile.type = 't'
        if type == u"Администратор": profile.type = 'a'

    birth_date = request.POST.get("birth_date")
    if birth_date != "" and validate(birth_date):
        profile.birth_date = birth_date

    github_id = request.POST.get("github_id")
    if github_id != "":
        profile.github_id = github_id

    stepic_id = request.POST.get("stepic_id")
    if stepic_id != "":
        profile.stepic_id = stepic_id

    election_date = request.POST.get("election_date")
    if election_date != "" and validate(election_date):
        profile.election_date = election_date

    contract_date = request.POST.get("contract_date")
    if contract_date != "" and validate(contract_date):
        profile.contract_date = contract_date

    academic_status = request.POST.get("academic_status")
    if academic_status != "":
        if academic_status == u"Ассистент": profile.academic_status = 'a'
        if academic_status == u"Старший преподаватель": profile.academic_status = 's'
        if academic_status == u"Доцент": profile.academic_status = 'd'
        if academic_status == u"Профессор": profile.academic_status = 'p'

    year_of_academic_status = request.POST.get("year_of_academic_status")
    if year_of_academic_status != "" and validate(year_of_academic_status):
        profile.year_of_academic_status = year_of_academic_status

    academic_degree = request.POST.get("academic_degree")
    if academic_degree != "":
        if academic_degree == u"Без степени": profile.academic_degree = 'n'
        if academic_degree == u"Кандидат наук": profile.academic_degree = 't'
        if academic_degree == u"Доктор наук": profile.academic_degree = 'd'

    year_of_academic_degree = request.POST.get("year_of_academic_degree")
    if year_of_academic_degree != "" and validate(year_of_academic_degree):
        profile.year_of_academic_degree = year_of_academic_degree

    profile.save()
    profile.user.save()

    context = {
        'profile': profile,
        'user': profile.user,
    }
    render(request, 'profileOpen.html', context)
    return HttpResponseRedirect('/profile')

@login_required(login_url="/login")
def profileCreate(request):
    user = User.objects.get(id=request.user.id)
    iProf = 0

    lastName = request.POST.get("lastName")
    if lastName != "": iProf+=1

    firstName = request.POST.get("firstName")
    if firstName != "": iProf+=1

    patronymic = request.POST.get("patronymic")
    if patronymic != "": iProf+=1

    type = request.POST.get("type")
    if type != "":
        if type == u"Преподаватель":
            type = 't'
            iProf += 1
        if type == u"Администратор":
            type = 'a'
            iProf += 1

    birth_date = request.POST.get("birth_date")
    if birth_date != "" and validate(birth_date): iProf+=1

    github_id = request.POST.get("github_id")
    if github_id != "": iProf+=1

    stepic_id = request.POST.get("stepic_id")
    if stepic_id != "": iProf+=1

    election_date = request.POST.get("election_date")
    if election_date != "" and validate(election_date): iProf+=1

    contract_date = request.POST.get("contract_date")
    if contract_date != "" and validate(contract_date): iProf+=1

    academic_status = request.POST.get("academic_status")
    if academic_status != "":
        if academic_status == u"Ассистент":
            academic_status = 'a'
            iProf += 1
        if academic_status == u"Старший преподаватель":
            academic_status = 's'
            iProf += 1
        if academic_status == u"Доцент":
            academic_status = 'd'
            iProf += 1
        if academic_status == u"Профессор":
            academic_status = 'p'
            iProf += 1

    year_of_academic_status = request.POST.get("year_of_academic_status")
    if year_of_academic_status != "" and validate(year_of_academic_status): iProf+=1

    academic_degree = request.POST.get("academic_degree")
    if academic_degree != "":
        if academic_degree == u"Без степени":
            academic_degree = 'n'
            iProf += 1
        if academic_degree == u"Кандидат наук":
            academic_degree = 't'
            iProf += 1
        if academic_degree == u"Доктор наук":
            academic_degree = 'd'
            iProf += 1

    year_of_academic_degree = request.POST.get("year_of_academic_degree")
    if year_of_academic_degree != "" and validate(year_of_academic_degree): iProf+=1

    if firstName!="": user.first_name = firstName
    if lastName!="": user.last_name = lastName
    user.save()

    if iProf == 11:
        user_profile = UserProfile.objects.create(
            user=user,
            patronymic=patronymic,
            birth_date=birth_date,
            github_id=github_id,
            stepic_id=stepic_id,
            type=type,
            election_date=election_date,
            contract_date=contract_date,
            academic_degree=academic_degree,
            year_of_academic_degree=year_of_academic_degree,
            academic_status=academic_status,
            year_of_academic_status=year_of_academic_status)

    render(request, 'profileOpen.html')
    return HttpResponseRedirect('/profile')

@login_required(login_url="/login")
def plan(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    publ = list(Publication.objects.filter(user_id=profile.id))
    # publ = Publication.objects.get(user_id=profile.id)
    context = {
        'publ': publ,
    }
    return render(request, 'plan.html', context)

@login_required(login_url="/login")
def listOfPlans(request):
    return render(request, 'listOfPlans.html')

@login_required(login_url="/login")
def accessNot(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'accessNot.html', context)

def managerReport(request):

    if request.user.is_superuser:
        return render(request,'manager/report.html')
    else:
        return HttpResponseRedirect("/accessNot")
