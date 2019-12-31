# coding:utf-8

import logging
from django.db import transaction
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status

from webkeyword.utils.api_response import JsonResponse
from webkeyword.utils.token_auth import get_user_id
from webkeyword.models import CaseGroup,Project
from webkeyword.serializers import CaseGroupSerializers,DesCaseGroupSerializers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import time


class CreateCaseGroupApi(APIView):

	def post(self,request):
		"""
		创建用例组接口
		:param request:
		:return:
		"""
		data = request.data
		serializer = CaseGroupSerializers(data=data)
		with transaction.atomic():
			if serializer.is_valid():
				create_time = str(time.time())[:10]
				data['createTime'] = create_time
				data['updateTime'] = create_time
				CaseGroup.objects.create(**data)
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="seccuss")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg="fail")

	def get(self, request):
		"""
        获取用例组列表接口
        :param request:
        :return:
        """
		projectId = request.GET.get('projectId', False)
		if not projectId:
			data = {'res': 'miss projectId params'}
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data, msg='fail')

		try:
			Project.objects.get(id=projectId)
		except:
			data = {'res': 'projectId:{} not found'.format(projectId)}
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data=data, msg='fail')
		try:
			page_size = int(request.GET.get('page_size', 20))
			page = int(request.GET.get('page', 1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)
		case_objects = CaseGroup.objects.filter(projectId=projectId)
		paginator = Paginator(case_objects, page_size)
		total = paginator.num_pages
		try:
			obm = paginator.page(page)
		except PageNotAnInteger:
			obm = paginator.page(1)
		except EmptyPage:
			obm = paginator.page(paginator.num_pages)
		serializer = CaseGroupSerializers(obm, many=True)
		return JsonResponse(code=status.HTTP_200_OK, data={
			"data": serializer.data,
			"page": page,
			"total": total
		}, msg="success")

class OpertionCaseGroupApi(APIView):
	# schema = CustomSchema()

	def get_objects(self,pk):
		try:
			return CaseGroup.objects.get(pk=pk)
		except:
			pass

	def get(self,request,pk):
		"""
		获取单个用例组接口
		:param request:
		:param pk:
		:return:
		"""
		pk_obj = self.get_objects(pk)

		seriailzer = DesCaseGroupSerializers(pk_obj)
		return JsonResponse(code=status.HTTP_200_OK,msg="seccuss",data=seriailzer.data)

	def put(self,request,pk):
		"""
		修改用例组接口
		:param request:
		:param pk:
		:return:
		"""
		pk_obj = self.get_objects(pk)
		if not pk_obj:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")
		data = request.data
		seriailzer = CaseGroupSerializers(pk_obj,data=request.data)
		with transaction.atomic():
			if seriailzer.is_valid():
				update_time = str(time.time())[:10]
				data['updateTime'] = update_time
				CaseGroup.objects.filter(id=pk).update(**data)
				return JsonResponse(code=status.HTTP_200_OK,data=seriailzer.data,msg="seccuss")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=seriailzer.errors,msg="fail")

	def delete(self,request,pk):
		"""
		删除用例组接口
		:param request:
		:param pk:
		:return:
		"""
		pk_obj = self.get_objects(pk)
		if not pk_obj:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res: not find pk:{0}".format(pk)},msg="fail")
		with transaction.atomic():
			pk_obj.delete()
			return JsonResponse(code=status.HTTP_200_OK,msg="success")