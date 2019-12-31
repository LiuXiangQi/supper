# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-27 10:49
# @Author : Dorom
# @File : http_common.py
# @Tag : 
# @Software: PyCharm
# -----------------*----------------- 

from rest_framework import status
from rest_framework.views import APIView
from webkeyword.models import CaseGroup
import abc


class HttpCommon(object):

    classmethod = abc.ABCMeta

    def host(self,caseGroupId):
        pass