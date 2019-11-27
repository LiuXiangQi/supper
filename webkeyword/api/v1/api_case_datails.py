# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-25 18:12
# @Author : Dorom
# @Site : 
# @File : api_case_datails.py
# @Tag : 用例执行步骤接口
# @Version : V1
# @Software: PyCharm
# -----------------*----------------- 

from rest_framework.views import APIView
from rest_framework import status
from webkeyword.serializers import CaseDatailsSerializers
from webkeyword.utils.api_response import JsonResponse

from webkeyword.models import CaseDatails
from webkeyword.utils.schema_view import CustomSchema


class CaseDatailsList(APIView):
	schema = CustomSchema()

	def post(self,request):
		"""
		添加用例操作步骤接口
		:param request: 接口参数
		:return:
		"""
		data = request.data
		serializer = CaseDatailsSerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(code=status.HTTP_200_OK,data = serializer.data)
		else:
			error = serializer.errors
		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg=error)


class CaseDatailsOpter(APIView):
	schema = CustomSchema()

	def get_object(self,pk):
		try:
			case_datails = CaseDatails.objects.get(pk=pk)
			return case_datails
		except:
			pass

	def get(self,request,pk):
		"""
		获取用例操作步骤
		:param request:
		:param pk: 操作步骤id
		:return:
		"""
		case_datails = self.get_object(pk)
		serializer = CaseDatailsSerializers(case_datails)
		return JsonResponse(code=status.HTTP_200_OK,data=serializer.data)

	def put(self,request,pk):
		"""
		修改用例操作步骤接口
		:param request:
		:param pk: 步骤id
		:return:
		"""
		case_datails = self.get_object(pk)
		serializer = CaseDatailsSerializers(case_datails,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(code=status.HTTP_200_OK,data=serializer.data)
		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=serializer.errors)

	def delete(self,request,pk):
		"""
		删除用例操作步骤接口
		:param request:
		:param pk: 操作步骤id
		:return:
		"""
		case_datails = self.get_object(pk)
		case_datails.delete()
		return JsonResponse(code=status.HTTP_200_OK)