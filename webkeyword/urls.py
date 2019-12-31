from django.conf.urls import url

from webkeyword.api.v1.auth_user import AuthUser
from webkeyword.api.v1.api_projects import CreateProjectApi,ProjectApi
from webkeyword.api.v1.api_case_group import CreateCaseGroupApi,OpertionCaseGroupApi
from webkeyword.api.v1.ui.api_case import CasePostApi,CaseApiOperate
from webkeyword.api.v1.ui.api_case_procedure import CaseDatailsList,CaseDatailsOpter
from webkeyword.api.v1.ui.api_start_case import StartCaseRun

from webkeyword.api.v1.interface.api_info import ApiInfoView,OpertionApiInfoView


urlpatterns = [
    url(r'v1/login$', AuthUser.as_view()),
	url(r'v1/projects$',CreateProjectApi.as_view()),
	url(r'v1/projects/(?P<pk>[0-9]+)/$',ProjectApi.as_view()),
	url(r'v1/case_group$',CreateCaseGroupApi.as_view()),
	url(r'v1/case_group/(?P<pk>[0-9]+)$',OpertionCaseGroupApi.as_view()),
	url(r'v1/test_case/ui$',CasePostApi.as_view()),
	url(r'v1/test_case/(?P<pk>[0-9]+)/ui$',CaseApiOperate.as_view()),
	url(r'v1/test_case_datails/ui$',CaseDatailsList.as_view()),
	url(r'v1/test_case_datails/(?P<pk>[0-9]+)/ui$', CaseDatailsOpter.as_view()),
	url(r'v1/test_case_run/ui$', StartCaseRun.as_view()),
    url(r'v1/api_info/api_auto$',ApiInfoView.as_view()),
    url(r'v1/api_info/(?P<caseId>[0-9]+)/(?P<seqId>[0-9]+)/api_auto$',OpertionApiInfoView.as_view())
]