# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-25 17:48
# @Author : Dorom
# @Site :  创建测试用例接口
# @File : api_case.py
# @Software: PyCharm
# -----------------*----------------- 


from django.db import transaction
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from rest_framework.views import APIView
from rest_framework import status

from webkeyword.utils.api_response import JsonResponse
from webkeyword.serializers import CaseSerializers
from webkeyword.models import Case



class CasePostApi(APIView):

	def post(self,request):
		"""
		创建用例接口
		:param request:
		:return:
		"""
		data = request.data
		serializers = CaseSerializers(data=data)
		with transaction.atomic():
			if serializers.is_valid():
				serializers.save()
				return JsonResponse(code=status.HTTP_200_OK,msg="success",data=data)
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data=serializers.errors)

	def get(self,request):
		data = request.data
		try:
			page_size = int(data.get('page_size',20))
			page = int(data.get('page',1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)
		case_objects = Case.objects.all()
		paginator = Paginator(case_objects, page_size)
		total = paginator.num_pages
		try:
			obm = paginator.page(page)
		except PageNotAnInteger:
			obm = paginator.page(1)
		except EmptyPage:
			obm = paginator.page(paginator.num_pages)
		serializer = CaseSerializers(obm,many=True)
		return JsonResponse(code=status.HTTP_200_OK,data={
			"data":serializer.data,
			"page": page,
			"total": total
		},msg="success")


class CaseApiOperate(APIView):

	def get_objects(self,pk):
		try:
			case_objects = Case.objects.get(pk=pk)
			return case_objects
		except:
			pass

	def get(self,pk):
		case_objects = self.get_objects(pk)
		serializer = CaseSerializers(case_objects)
		return JsonResponse(code=status.HTTP_200_OK,msg="success",data=serializer.data)

	def put(self,request,pk):
		case_objects = self.get_objects(pk)
		serializer = CaseSerializers(case_objects,data=request.data)
		with transaction.atomic():
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(code=status.HTTP_200_OK,msg="success",data=serializer.data)
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data=serializer.errors)

	def delete(self,pk):
		case_objects = self.get_objects(pk)
		serializer = CaseSerializers(case_objects)
		with transaction.atomic():
			serializer.delete()
			return JsonResponse(code=status.HTTP_200_OK,msg="success")
