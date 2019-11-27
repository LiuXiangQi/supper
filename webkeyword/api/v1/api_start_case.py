# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-25 17:49
# @Author : Dorom
# @Site : 
# @File : api_start_case.py
# @Software: PyCharm
# -----------------*----------------- 


from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from webkeyword.utils.api_response import JsonResponse
from webkeyword.utils.token_auth import get_user_id
from webkeyword.serializers import CaseSerializers,CaseUpdateSerializers
from webkeyword.models import Case,CaseGroup


class StartCaseRun(APIView):
	pass
