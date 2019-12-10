# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-25 17:49
# @Author : Dorom
# @Site : 
# @File : api_start_case.py
# @Software: PyCharm
# -----------------*----------------- 


from rest_framework.views import APIView
from rest_framework import status
from webkeyword.utils.api_response import JsonResponse
from webkeyword.utils.token_auth import get_user_id
from webkeyword.serializers import StartCaseSeriailzers
from webkeyword.models import Project,Case,CaseGroup,CaseProcedure,GlobalData,CheckCase
from webkeyword.utils.UIAutoCommon.runcommon import InternalDataStorage,ExecuteMain
from webkeyword.utils.UIAutoCommon.browser import Browser


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
		"""获取用例下所有的操作步骤id,并根据step大小正序排列
		:param caseId:
		:return:
		"""
		case_procedure_list_query = CaseProcedure.objects.filter(caseId=caseId)
		case_procedure_list_query_li = case_procedure_list_query.all().order_by('step')
		return case_procedure_list_query_li

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

			destUrl = data.get('destUrl')
			browserType = data.get('browserType')
			webdriverPath = data.get('webdriverPath')

			dest_url_querySet = GlobalData.objects.filter(name=destUrl)
			if not dest_url_querySet:
				return JsonResponse(code=status.HTTP_200_OK, data={'res': "destUrl: {0}  不存在".format(destUrl)},
									msg="seccuss")
			# 检查全局参数是否合法
			browser_querySet = GlobalData.objects.filter(name=browserType)
			if not browser_querySet:
				return JsonResponse(code=status.HTTP_200_OK, data={'res': "browserType: {0}  不存在".format(browserType)},
									msg="seccuss")
			webdriverPath_querySet = GlobalData.objects.filter(name=webdriverPath)

			if not webdriverPath_querySet:
				return JsonResponse(code=status.HTTP_200_OK, data={'res': "webdriverPath: {0}  不存在".format(webdriverPath)},
									msg="seccuss")
			dest_url = dest_url_querySet.first().params
			browser_data = browser_querySet.first().params
			webdriver_data = webdriverPath_querySet.first().params

			driver = Browser().open_broswer(browser_data,webdriver_data,dest_url)

			case_procedure_list_query_li = self.get_case_procedure(caseId)
			if not case_procedure_list_query_li:
				return JsonResponse(code=status.HTTP_200_OK, data={'res': "case: {0} 用例没有操作步骤".format(caseId)},
									msg="seccuss")
			# 用于初始化，记录用例的全局内部数据
			internal_data_storage = InternalDataStorage()

			# 执行用例的所有步骤
			for case_procedure_list_query in case_procedure_list_query_li:
				try:
					ExecuteMain(driver).run(case_procedure_list_query,internal_data_storage)
					result = "步骤执行完成"
				except Exception as e:
					result = "步骤执行失败：{0}".format(e)
				# 记录步骤执行结果
				CaseProcedure.objects.filter(id=case_procedure_list_query.id).update(result=result)

			driver.close()

		#最后整体用例检查是否成功
		check_result_object = CheckCase.objects.filter(caseId=caseId)
		result_li = []
		for check_result in check_result_object:
			result = check_result.check_result
			result_li.append(result)
		if "False" in result_li:
			return JsonResponse(code=status.HTTP_200_OK, msg="fail", data={'res': result_li})
		else:
			return JsonResponse(code=status.HTTP_200_OK, msg="seccuss", data={'res': '200'})

