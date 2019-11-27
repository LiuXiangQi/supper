
from django.shortcuts import render

# Create your views here.

import time
from webkeyword.models import *
from django.http import JsonResponse
from rest_framework.views import APIView



# 视图
from webkeyword.models import User,Project
from rest_framework import viewsets
from  webkeyword.serializers import UserSerializers

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    '''查看，编辑用户的界面'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializers

class GroupViewSet(viewsets.ModelViewSet):
    '''查看，编辑组的界面'''
    queryset = Project
    # serializer_class = ProjectDesSerializers