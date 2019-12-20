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
from webkeyword.serializers import CaseProcedureSerializers
from webkeyword.utils.api_response import JsonResponse

from webkeyword.models import CaseProcedure,Case
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


class CaseDatailsList(APIView):

	def check_params(self,caseId,step):
		"""
		用于检测一个用例的步骤是否已存在
		:param caseId:
		:param step:
		:return: 查询结果
		"""
		try:
			case_id_obj = Case.objects.get(id=caseId)
		except:
			return JsonResponse(code=status.HTTP_201_CREATED, data={
				"res": "caseId is not exit"
			}, msg='fail')

		res = CaseProcedure.objects.filter(caseId=caseId,step=step)
		if res:
			return JsonResponse(code=status.HTTP_201_CREATED, data={
				"res": "step is exit"
			}, msg='fail')


	def post(self,request):
		"""
		添加用例操作步骤接口
		:param request: 接口参数
		:return:
		"""
		data = request.data
		serializer = CaseProcedureSerializers(data=data)
		if serializer.is_valid():
			caseId = data.get("caseId")
			step = data.get("step")
			res = self.check_params(caseId,step)
			if res:
				return res
			serializer.save()
			return JsonResponse(code=status.HTTP_200_OK,data = serializer.data,msg='seccuss')

		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg= serializer.errors)

	def get(self,request):
		"""
		获取全部用例执行步骤
		:param request:
		:return:
		"""
		caseId = request.GET.get('caseId',False)
		try:
			page_size = int(request.GET.get('page_size',20))
			page = int(request.GET.get('page',20))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)

		case_objects = CaseProcedure.objects.filter(caseId=caseId)
		paginator = Paginator(case_objects, page_size)
		total = paginator.num_pages
		try:
			obm = paginator.page(page)
		except PageNotAnInteger:
			obm = paginator.page(1)
		except EmptyPage:
			obm = paginator.page(paginator.num_pages)
		serializer = CaseProcedureSerializers(obm,many=True)
		return JsonResponse(code=status.HTTP_200_OK,data={
			"data":serializer.data,
			"page": page,
			"total": total
		},msg="success")


class CaseDatailsOpter(APIView):

	def get_object(self,pk):
		try:
			case_datails = CaseProcedure.objects.get(id=pk)
			return case_datails
		except Exception as e:
			pass

	def get(self,request,pk):
		"""
		获取用例单个操作步骤
		:param request:
		:param pk: 操作步骤id
		:return:
		"""
		case_datails = self.get_object(pk)
		serializer = CaseProcedureSerializers(case_datails)
		return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="success")

	def put(self,request,pk):
		"""
		修改用例操作步骤接口
		:param request:
		:param pk: 步骤id
		:return:
		"""
		case_datails = self.get_object(pk)
		if not case_datails:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")

		serializer = CaseProcedureSerializers(case_datails, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(code=status.HTTP_200_OK, data=serializer.data,msg="success")
		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=serializer.errors)

	def delete(self,request,pk):
		"""
		删除用例操作步骤接口
		:param request:
		:param pk: 操作步骤id
		:return:
		"""
		try:
			case_datails = self.get_object(pk)
			if not case_datails:
				return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")
			case_datails.delete()
			return JsonResponse(code=status.HTTP_200_OK,msg="success")
		except:
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg="未知错误")