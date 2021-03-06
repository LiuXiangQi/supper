"""superproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,re_path
from rest_framework import routers

from webkeyword import urls
from webkeyword import views
from webkeyword.utils.schema_view import schema_view

from webkeyword.route.route import index,login


#路由
# router = routers.DefaultRouter()
# router.register(r'users',views.UserViewSet,base_name='user')
# router.register(r'Project',views.GroupViewSet,base_name='Project')



# 重要的是如下三行
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='自动化测试平台接口', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', schema_view, name="docs"),
    path('admin/', admin.site.urls),
    url(r'^api/',include(urls)),
    url(r'login',login),
    url(r'^$',index),
]