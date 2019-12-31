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
				return JsonResponse(code=status.HTTP_200_OK,data=data,msg="success")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializers.errors,msg='fail')

	def get(self,request):
		"""
		获取用例列表接口
		:param request:
		:return:
		"""
		try:
			page_size = int(request.GET.get('page_size',20))
			page = int(request.GET.get('page',1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)

		caseGroupId = int(request.GET.get('caseGroupId',0))
		if isinstance(caseGroupId,int):
			if caseGroupId:
				case_objects = Case.objects.filter(caseGroupId=caseGroupId)
			else:
				case_objects = Case.objects.all()
		else:
			res = "caseGroupId must be int"
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data= {'res':res},msg='fail')

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

	def get(self,request,pk):
		"""
		获取单个用例接口
		:param request:
		:param pk:
		:return:
		"""
		case_objects = self.get_objects(pk)
		serializer = CaseSerializers(case_objects)
		return JsonResponse(code=status.HTTP_200_OK,msg="success",data=serializer.data)

	def put(self,request,pk):
		"""
		修改用例接口
		:param request:
		:param pk:
		:return:
		"""
		case_objects = self.get_objects(pk)
		if not case_objects:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")

		serializer = CaseSerializers(case_objects,data=request.data)
		with transaction.atomic():
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="success")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg='fail')

	def delete(self,request,pk):
		"""
		删除用例接口
		:param pk:
		:return:
		"""
		case_objects = self.get_objects(pk)
		if not case_objects:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")
		with transaction.atomic():
			case_objects.delete()
			return JsonResponse(code=status.HTTP_200_OK,msg="success")