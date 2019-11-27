# coding:utf-8

import logging
from django.db import transaction

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from rest_framework.views import APIView
from rest_framework import status

from webkeyword.utils.api_response import JsonResponse
from webkeyword.models import Project,User,UserToken
from webkeyword.serializers import ProjectSerializers

class CreateProjectApi(APIView):
	def post(self,request):
		data = request.data
		serializer = ProjectSerializers(data=data)
		with transaction.atomic():
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg='success')
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg="fail")

class ProjectApi(APIView):
	def get_objects(self,pk):
		try:
			return Project.objects.get(pk=pk)
		except:
			pass

	def get(self,request,pk):
		"""
		获取单个项目接口
		:param request:
		:param pk: 项目id
		:return:
		"""
		project_objects = self.get_objects(pk)
		serializer = ProjectSerializers(project_objects,many=True)
		return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="success")

	def put(self,request,pk):
		"""
		修改项目接口
		:param request:
		:param pk: 项目id
		:return:
		"""
		data = request.data
		project_objects = self.get_objects(pk)
		serializer = ProjectSerializers(project_objects,data=data)
		with transaction.atomic():
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg='success')
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data=serializer.errors)

	def delete(self,request,pk):
		"""
		删除项目接口
		:param request: 请求
		:param pk: 项目id
		:return:
		"""
		project_objects = self.get_objects(pk)
		serializer = ProjectSerializers(project_objects)
		with transaction.atomic():
			serializer.delete()
			return JsonResponse(code=status.HTTP_200_OK, msg="success")

