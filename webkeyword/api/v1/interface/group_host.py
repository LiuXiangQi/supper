# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-27 10:55
# @Author : Dorom
# @File : group_host.py
# @Tag : 
# @Software: PyCharm
# -----------------*----------------- 

from rest_framework import status
from rest_framework.views import APIView
from webkeyword.models import CaseGroup
from webkeyword.serializers import CaseGroupHostSerializer
from webkeyword.utils.api_response import JsonResponse
from django.db import transaction
class CaseGroupHostView(APIView):

    def check_caseGroupId(self,case_group_id):
        try:
            CaseGroup.objects.get(id=case_group_id)
        except:
            data = {'res':'caseGroupId not exiest'}
            return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=data,msg='fail')

    def post(self,request):
        data = request.data
        serializer = CaseGroupHostSerializer(data=data)
        if serializer.is_valid():
            case_group_id = data.get('caseGroupId')
            if case_group_id:
                return case_group_id
            with transaction.atomic():
                pass