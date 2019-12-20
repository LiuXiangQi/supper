# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-30 10:26
# @Author : Dorom
# @Site : 
# @File : api_global_params.py
# @Tag : 
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 

from rest_framework.views import APIView
from rest_framework import status
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from webkeyword.models import GlobalData
from webkeyword.utils.api_response import JsonResponse
from webkeyword.serializers import GlobalParamsSerializers



class GlobalParamsApi(APIView):

	def get(self,request):
		"""
		查询所有全局参数列表
		:param request:
		:return:
		"""
		data = request.data
		try:
			page_size = request.GET.get('page_size',20)
			page = int(request.GET.get('page',1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)


		qurieyset = GlobalData.objects.all()
		paginator = Paginator(qurieyset,page_size)
		total = paginator.num_pages
		try:
			obj = paginator.page(page_size)
		except PageNotAnInteger:
			obj = paginator.page(1)
		except EmptyPage:
			obj = paginator.page(paginator.num_pages)

		serializer = GlobalParamsSerializers(obj,many=True)
		return JsonResponse(code=status.HTTP_200_OK,data={
			"data":serializer.data,
			"page":page,
			"total":total
		},msg="success")

	def post(self,request):
		"""
		添加全局参数接口
		:param request:
		:return:
		"""
		data = request.data
		serializers = GlobalParamsSerializers(data=data)
		if serializers.is_valid():
			serializers.save()
			return JsonResponse(code=status.HTTP_200_OK,data=serializers.data,msg='seccuss')
		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializers.errors,msg='fail')


class GlobalParamsQureyApi(APIView):

	def check_query_obj(self,pk):
		queryset = GlobalData.objects.filter(pk=pk)
		return queryset

	def get(self,request,pk):
		queryset = self.check_query_obj(pk)
		if not queryset:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND,data={"res":"没有id为：{}的数据".format(pk)},msg="fail")
		serialzers = GlobalParamsSerializers(queryset)
		return JsonResponse(code=status.HTTP_200_OK,data=serialzers.data,msg="seccuss")

	def put(self,request,pk):
		data = request.data
		queryset = self.check_query_obj(pk)
		if not queryset:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND,data={"res":"没有id为：{}的数据".format(pk)},msg="fail")
		serialzers = GlobalParamsSerializers(queryset,data=data)
		if serialzers.is_valid():
			serialzers.save()
			return JsonResponse(code=status.HTTP_200_OK,data=serialzers.data,msg="success")
		return JsonResponse(code=status.HTTP_502_BAD_GATEWAY,data=serialzers.errors,msg="fail")


	def delete(self,request,pk):
		queryset = self.check_query_obj(pk)
		if not queryset:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res": "删除的数据不存在".format(pk)},
								msg="fail")
		queryset.delete()
		return JsonResponse(code=status.HTTP_200_OK,msg="success")