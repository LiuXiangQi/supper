from django.urls import path
from django.conf.urls import url,re_path

from webkeyword.api.v1.auth_user import AuthUser
from webkeyword.api.v1.api_projects import ProjectApi
from webkeyword.api.v1.api_case_group import CreateCaseGroupApi,OpertionCaseGroupApi
from webkeyword.api.v1.api_case import CasePostApi,CaseApiOperate
from webkeyword.api.v1.api_case_datails import CaseDatailsList,CaseDatailsOpter


urlpatterns = [
    url(r'v1/auth$', AuthUser.as_view()),
	url(r'v1/projects$',ProjectApi.as_view()),
	url(r'v1/case_group$',CreateCaseGroupApi.as_view()),
	url(r'v1/case_grou/(?P<pk>[0-9]+)$',OpertionCaseGroupApi.as_view()),
	url(r'v1/test_case$',CasePostApi.as_view()),
	url(r'v1/test_case/(?P<pk>[0-9]+)$',CaseApiOperate.as_view()),
	url(r'v1/test_case_datails$',CaseDatailsList.as_view()),
	url(r'v1/test_case_datails/(?P<pk>[0-9]+)$', CaseDatailsOpter.as_view())
]
