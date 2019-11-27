# coding:utf-8

import logging
from django.db import transaction
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status

from webkeyword.utils.api_response import JsonResponse
from webkeyword.utils.token_auth import get_user_id
from webkeyword.models import CaseGroup
from webkeyword.serializers import CaseGroupSerializers
from webkeyword.utils.schema_view import CustomSchema


class CreateCaseGroupApi(APIView):
	schema = CustomSchema()

	def post(self,request):
		data = request.data
		serializer = CaseGroupSerializers(data=data)
		with transaction.atomic():
			if serializer.is_valid():
				serializer.save()
				return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="seccuss")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg="fail")

	def get(self,request):
		data = request.data
		try:
			page_size = int(data.get('page_size',20))
			page = int(data.get('page',1))
		except Exception as ex:
			return JsonResponse(code=status.HTTP_400_BAD_REQUEST, msg=ex)
		case_objects = CaseGroup.objects.all()
		paginator = Paginator(case_objects, page_size)
		total = paginator.num_pages
		try:
			obm = paginator.page(page)
		except PageNotAnInteger:
			obm = paginator.page(1)
		except EmptyPage:
			obm = paginator.page(paginator.num_pages)
		serializer = CaseGroupSerializers(obm,many=True)
		return JsonResponse(code=status.HTTP_200_OK,data={
			"data":serializer.data,
			"page": page,
			"total": total
		},msg="success")

class OpertionCaseGroupApi(APIView):
	schema = CustomSchema()

	def get_objects(self,pk):
		try:
			return CaseGroup.objects.get(pk=pk)
		except:
			pass

	def get(self,pk):
		pk_obj = self.get_objects(pk)
		seriailzer = CaseGroupSerializers(pk_obj)
		return JsonResponse(code=status.HTTP_200_OK,msg="seccuss",data=seriailzer.data)

	def patch(self,request,pk):
		pk_obj = self.get_objects(pk)
		seriailzer = CaseGroupSerializers(pk_obj,data=request.data)
		with transaction.atomic():
			if seriailzer.is_valid():
				seriailzer.save()
				return JsonResponse(code=status.HTTP_200_OK,data=seriailzer.data,msg="seccuss")
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=seriailzer.errors,msg="fail")

	def delete(self,pk):
		pk_obj = self.get_objects(pk)
		seriailzer = CaseGroupSerializers(pk_obj)
		with transaction.atomic():
			seriailzer.delete()
			return JsonResponse(code=status.HTTP_200_OK,msg="success")