from django.conf.urls import patterns, url
from django.conf.urls import url, include
from django.contrib.contenttypes import views as contenttype_views
from views import *

urlpatterns = patterns(
   '',
   url(r'^$', index, name='tpindex'),
   url(r'^login$', loginTeacher, name='tplogin', ),
   url(r'^profile$', profileOpen, name='tpprofile'),
   url(r'^profilesave$', profileSave, name='tpprofilesave'),
   url(r'^profileCreate$', profileSave, name='tpprofileCreate'),
   url(r'^loginwitherror$', errorLoginTeacher, name='tploginwitherror', ),
   url(r'^logout$', logoutTeacher, name='tplogout', ),
   url(r'^listOfPlans$', listOfPlans, name='tpplanlist', ),
   url(r'^makeNewPlan$', makeNewPlan, name='tpnewPlan', ),
   url(r'^deletePlan$', deletePlan, name='tpdeletePlan', ),
   url(r'^makeNewPlanSaveNIR$', makeNewPlanSaveNIR, name='tpnewPlanSaveNIR', ),
   url(r'^makeNewPlanSavePublication$', makeNewPlanSavePublication, name='tpnewPlanSavePublication', ),
   url(r'^makeNewPlanSaveQual$', makeNewPlanSaveQual, name='tpnewPlanSaveQual', ),
   url(r'^makeNewPlanSaveOther$', makeNewPlanSaveOther, name='tpnewPlanSaveOther', ),
   url(r'^makeNewPlanSaveBook$', makeNewPlanSaveBook, name='tpnewPlanSaveBook', ),
   url(r'^makeNewPlanSaveScience$', makeNewPlanSaveScience, name='tpnewPlanSaveScience', ),
   url(r'^makeNewPlanSaveDisc$', makeNewPlanSaveDisc, name='tpnewPlanSaveDisc', ),
   url(r'^plan$', plan, name='tpplan', ),
   url(r'^accessNot$', accessNot, name='tpaccessNot', ),
   url(r'^managerReport$', managerReport, name='tpsimpleReport'),
   url(r'^reports$', userReport, name='tpuserReport')
)

