# coding:utf-8

import logging
from django.db import transaction

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from rest_framework.views import APIView
from rest_framework import status

from webkeyword.utils.api_response import JsonResponse
from webkeyword.models import Project,User,UserToken
from webkeyword.serializers import ProjectSerializers,DesProjectSerializers
import time


class CreateProjectApi(APIView):
	def post(self,request):
		"""
		创建项目接口
		:param request:
		:return:
		"""
		data = request.data
		serializer = ProjectSerializers(data=data)
		with transaction.atomic():
			if serializer.is_valid():
				create_time = time.time()[:10]
				data['createTime'] = create_time
				data['updateTime'] = create_time
				Project.objects.create(**data)
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg='success')
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg="fail")

	def get(self, request):
		"""
        获取项目接口
        :param request:
        :return:
        """
		try:
			page_size = int(request.GET.get('page_size', 20))
			page = int(request.GET.get('page', 1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)

		ProjectsId = request.GET.get('id', '0')
		if isinstance(ProjectsId, int):
			if ProjectsId:
				Projectqueryset = Project.objects.filter(id=ProjectsId)
			else:
				Projectqueryset = Project.objects.all()
		else:
			res = "id  must be int"
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={'res': res}, msg='fail')

		paginator = Paginator(Projectqueryset, page_size)
		total = paginator.num_pages
		try:
			obm = paginator.page(page)
		except PageNotAnInteger:
			obm = paginator.page(1)
		except EmptyPage:
			obm = paginator.page(paginator.num_pages)
		serializer = DesProjectSerializers(obm, many=True)
		return JsonResponse(code=status.HTTP_200_OK, data={
			"data": serializer.data,
			"page": page,
			"total": total
		}, msg="success")


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
		serializer = DesProjectSerializers(project_objects)
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
				update_time = time.time()[:10]
				data['updateTime'] = update_time
				Project.objects.filter(id=pk).update(**data)
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg='success')
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data=serializer.errors)

	def delete(self,request,pk):
		"""
		删除项目接口
		:param request: 请求
		:param pk: 项目id
		:return:
		"""
		try:
			project_objects = self.get_objects(pk)
			with transaction.atomic():
				project_objects.delete()
				return JsonResponse(code=status.HTTP_200_OK, msg="success")
		except:
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg="未知错误")

