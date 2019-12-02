# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-25 17:49
# @Author : Dorom
# @Site : 
# @File : api_start_case.py
# @Software: PyCharm
# -----------------*----------------- 


from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from webkeyword.utils.api_response import JsonResponse
from webkeyword.utils.token_auth import get_user_id
from webkeyword.serializers import StartCaseSeriailzers
from webkeyword.models import Project,Case,CaseGroup,CaseProcedure


class StartCaseRun(APIView):

	def check_params(self,data):
		"""
		执行用例，检查参数的有效性
		:param data: projectId、caseGroupId、caseId 是否有效
		:return:
		"""
		projectId = data.get("projectId")
		try:
			project_queryset = Project.objects.get(id=projectId)
		except:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND,
								data={"res":"projectId:{0} not exist".format(projectId)},
								msg="fail")
		caseGroupId = data.get("caseGroupId")
		try:
			caseGroup_queryset = CaseGroup.objects.get(id=caseGroupId)
		except:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND,
								data={"res":"caseGroupId:{0} not exist".format(caseGroupId)},
								msg="fail")

		caseId = data.get("caseId")
		try:
			case_queryset = Case.objects.get(id=caseId)
		except:
			return JsonResponse(code=status.HTTP_404_NOT_FOUND,
								data={"res": "CaseId:{0} not exist".format(caseId)},
								msg="fail")

	def get_case_procedure(self,caseId):
		"""
		获取用例下所有的操作步骤id
		:param caseId:
		:return:
		"""
		case_procedure_list_query = CaseProcedure.objects.filter(CaseId=caseId)
		return case_procedure_list_query

	def post(self,request):
		"""
		执行单个测试用例接口
		:param request:
		:return:
		"""
		data = request.data
		seriailzers = StartCaseSeriailzers(data=data)
		if seriailzers.is_valid():
			result = self.check_params(seriailzers.data)
			if result:
				return result
			caseId = data.get('caseId')
			caseGroupId = data.get('caseGroupId')
			caseId =  Case.objects.filter(id=caseId,caseGroupId=caseGroupId).first().id
			case_procedure_list_query = self.get_case_procedure(caseId)
			# TODO case_procedure_list_query 获取到单个用例的所有操作步骤，等待执行
			return JsonResponse(code=status.HTTP_200_OK,msg="seccuss")
		return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=seriailzers.errors,msg="fail")