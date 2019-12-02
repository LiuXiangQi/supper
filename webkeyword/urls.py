from django.urls import path
from django.conf.urls import url,re_path

from webkeyword.api.v1.auth_user import AuthUser
from webkeyword.api.v1.api_projects import CreateProjectApi,ProjectApi
from webkeyword.api.v1.api_case_group import CreateCaseGroupApi,OpertionCaseGroupApi
from webkeyword.api.v1.api_case import CasePostApi,CaseApiOperate
from webkeyword.api.v1.api_case_procedure import CaseDatailsList,CaseDatailsOpter
from webkeyword.api.v1.api_start_case import StartCaseRun


urlpatterns = [
    url(r'v1/auth$', AuthUser.as_view()),
	url(r'v1/projects$',CreateProjectApi.as_view()),
	url(r'v1/projects/(?P<pk>[0-9]+)$',ProjectApi.as_view()),
	url(r'v1/case_group$',CreateCaseGroupApi.as_view()),
	url(r'v1/case_group/(?P<pk>[0-9]+)$',OpertionCaseGroupApi.as_view()),
	url(r'v1/test_case$',CasePostApi.as_view()),
	url(r'v1/test_case/(?P<pk>[0-9]+)$',CaseApiOperate.as_view()),
	url(r'v1/test_case_datails$',CaseDatailsList.as_view()),
	url(r'v1/test_case_datails/(?P<pk>[0-9]+)$', CaseDatailsOpter.as_view()),
	url(r'v1/test_case_run$', StartCaseRun.as_view())
]