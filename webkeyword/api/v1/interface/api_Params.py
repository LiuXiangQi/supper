# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-24 20:08
# @Author : Dorom
# @File : api_Params.py
# @Tag :  接口添加params 参数
# @Software: PyCharm
# -----------------*----------------- 
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from webkeyword.serializers import ApiParamsSerializer
from webkeyword.utils.api_response import JsonResponse
from webkeyword.models import ApiInfo


class ApiParamsView(APIView):
    def check_api_id(self,api):
        try:
            return ApiInfo.objects.get(api)
        except:
            return None

    def post(self,request):
        data = request.data
        serializers = ApiParamsSerializer(data=data)
        with transaction.atomic():
            if serializers.is_valid():
                api_id = data.get("api")
                api_id = self.check_api_id(api_id)
                if not api_id:
                    data = {'res':'api id not is exist'}
                    return JsonResponse(code=status.HTTP_404_NOT_FOUND,data=data,msg="fail")
                serializers.save()
                return JsonResponse(code=status.HTTP_200_OK,msg='seccuss',data=serializers.data)
            return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data=serializers.errors)