# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-06 16:29
# @Author : Dorom
# @Site : 
# @File : runcommon.py
# @Tag : 
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 


from webkeyword.models import CaseProcedure,CheckCase
from webkeyword.UIAutoCommon.case_step_judge import JudgeHolder
from webkeyword.utils.api_response import JsonResponse
from webkeyword.UIAutoCommon.website_key_word import UIKeyWordMain
from webkeyword.utils.logger import logger
from rest_framework import status

class InternalDataStorage(object):
	"""
	用于存储整个测试用例的 元素返回数据
	"""
	def __init__(self):
		self.data = {}
		self.exit_li = []



class ExecuteDataHodler():
	""" 这个类 只是用来初始化用例步骤对象的作用，用于存储步骤属性，实现数据共享
	"""
	def __init__(self,driver):
		self.driver = driver
		self.key_word = None
		self.case_id = None
		self.element = None
		self.send_key_value = None
		self.step = None
		self.judge_step_set = None
		self.judge_key_word = None
		self.judge_value = None
		self.link_step_id = None
		self.for_step_set = None
		self.not_run_step = []
		self.id = None
		self.returnValue = None

	def get_case_procedure_data(self,case_procedure_list_query):
		"""
		数据初始化
		:param case_procedure_list_query: 步骤query对象
		:return:
		"""
		self.id = case_procedure_list_query.id
		self.case_id = case_procedure_list_query.caseId
		self.key_word = case_procedure_list_query.KeyWord
		self.element = case_procedure_list_query.element
		self.send_key_value = case_procedure_list_query.send_key_value
		self.step = case_procedure_list_query.step
		self.judge_step_set = case_procedure_list_query.judge_step_set
		self.judge_key_word = case_procedure_list_query.judge_key_word
		self.judge_value = case_procedure_list_query.judge_value
		self.link_step_id = case_procedure_list_query.link_step_id
		self.for_step_set = case_procedure_list_query.for_step_set
		self.check_result_status = case_procedure_list_query.check_result_status
		self.check_result_step = case_procedure_list_query.check_result_step



class ExecuteKeyWordFunc(object):

	def key_word_run_func(self,classHolder,internal_data_storage):
		"""
		1、关键字元素方法执行，如果 self.link_step_id（关联的上下文步骤的id） 存在，同时本id（步骤id）的self.element（目标元素）
		为空时， self.element = self.returnValue
		2、检查self.send_key_value（输入的字符串内容） 是否存在 如果存在调用方法传参需要加上self.send_key_value 参数，如果不存在
		则不传，
		3、无论关键字元素操作的返回值res是否为None，都会更新本步骤的returnValue字段
		: params classHolder  classHolder类对象
		: params internal_data_storage  InternalDataStorage类对象 用于数据存储
		:return:
		"""
		logger.info("正在执行用例:{0}的第{1}个步骤".format(classHolder.case_id,classHolder.id))
		link_id = classHolder.link_step_id
		if link_id:
			if not classHolder.element:
				link_id_quiryset = CaseProcedure.objects.filter(id=link_id)
				if not link_id_quiryset:
					res = {'res':"link_step_id:{0} 映射的caseId not found".format(classHolder.link_step_id)}
					return JsonResponse(code=status.HTTP_404_NOT_FOUND,
										data=res,msg="fail")

				link_data = internal_data_storage.data.get(link_id)
				classHolder.element = link_data

		send_key_value = classHolder.send_key_value

		if send_key_value:
			res = UIKeyWordMain(classHolder.driver).run_key_word_main(classHolder.key_word,classHolder.element,send_key_value)
		else:
			logger.info("开始使用关键字:{0} 操作元素{1}".format(classHolder.key_word,classHolder.element))
			ui_key_word_main = UIKeyWordMain(classHolder.driver)
			res = ui_key_word_main.run_key_word_main(classHolder.key_word,classHolder.element)

		# 更新内存数据，便于关联上下文
		internal_data_storage.data[str(classHolder.id)] = res
		logger.info("用例:{0} 步骤：{1}时内存总记录的数据:{2}".format(classHolder.case_id,classHolder.id,str(internal_data_storage.data)))



class ExecuteMain(object):
	def __init__(self,driver):
		self.driver = driver
		self.execute_data_holder = ExecuteDataHodler(driver)
		self.judge_res = None

	def execute_for_main(self,internal_data_storage,for_step):
		"""
		for 循环步骤
		:param internal_data_storage:
		:param for_step:
		:return:
		"""
		for_step_li = eval(for_step)
		for for_step in for_step_li:
			internal_data_storage.exit_li.append(for_step)
			case_procedure_list_query = CaseProcedure.objects.filter(id=for_step)
			# 退出for循环
			if self.execute_data_holder.element == "back":
				break
			self.run(case_procedure_list_query[0], internal_data_storage)

	def execute_if_main(self,internal_data_storage):
		"""
		判断语句的执行步骤
		:param internal_data_storage:
		:return:
		"""
		judge_step_li = self.execute_data_holder.judge_step_set
		if judge_step_li:
			li = eval(self.execute_data_holder.judge_step_set)
			for step in li:
				case_procedure_list_query = CaseProcedure.objects.filter(id=step)
				self.run(case_procedure_list_query[0], internal_data_storage)
				internal_data_storage.exit_li.append(step)

	def execute_check_main(self):
		"""
		检查点执行
		:return:
		"""
		self.execute_data_holder.check_result_step = eval(self.execute_data_holder.check_result_step)
		# 如果执行步骤id 等于检查点最后的执行步骤id，就记录测试结果
		if self.execute_data_holder.step == self.execute_data_holder.check_result_step[-1]:
			# 记录检查点结果
			check_case_report_obj = CheckCase(caseId=self.execute_data_holder.case_id,
											  seq=self.execute_data_holder.step,
											  check_result=self.judge_res)
			check_case_report_obj.save()

	def run(self,case_procedure_list_query,internal_data_storage):
		"""
		:param case_procedure_list_query:
		:param internal_data_storage: 用例全局数据保存在内存的对象
		:return:
		"""
		# 获取该步骤的所有属性
		self.execute_data_holder.get_case_procedure_data(case_procedure_list_query)
		# 执行步骤id 不在已经执行步骤的 判断步骤里
		if self.execute_data_holder.id not in internal_data_storage.exit_li:
			# 有ele 元素的关键字操作
			ExecuteKeyWordFunc().key_word_run_func(self.execute_data_holder,internal_data_storage)
			judge_key_word = self.execute_data_holder.judge_key_word
			if judge_key_word:
				id = str(self.execute_data_holder.id)
				search_value = str(internal_data_storage.data.get(id))
				judge_value = str(self.execute_data_holder.judge_value)
				self.judge_res = JudgeHolder().start_judge(judge_key_word,search_value,judge_value)

			# 是否为检查点
			status = self.execute_data_holder.check_result_status
			if status == "True":
				self.execute_check_main()

			# 执行操作步骤的for循环语句
			for_step = self.execute_data_holder.for_step_set
			if for_step:
				self.execute_for_main(internal_data_storage,for_step)

			# 如果判断语句条件成立
			if self.judge_res:
				self.execute_if_main(internal_data_storage)