# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-28 15:28
# @Author : Dorom
# @Site : 
# @File : case_step_judge.py
# @Tag : 用例步骤判断方法集合
# @Version : 1.1
# @Software: PyCharm
# -----------------*----------------- 

from webkeyword.utils.errorException import *
from webkeyword.utils.db_connect import DbOption
import abc

class Judge(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def judge(self,*args,**kwargs):
		pass


class GreaterThan(Judge):
	"""
	大于的业务条件判断
	"""
	def judge(self,search_value,judge_value):
		if search_value>judge_value:
			return True
		else:
			return False


class LessThan(Judge):
	"""
	小于的业务条件判断
	"""
	def judge(self,search_value,judge_value):
		if search_value<judge_value:
			return True
		else:
			return False


class EqualAndGreaterThan(Judge):
	"""
	大于等于的业务条件判断
	"""

	def judge(self, search_value, judge_value):
		if search_value >=judge_value:
			return True
		else:
			return False


class EqualOrLessThan(Judge):
	"""
	小于等于的业务条件判断
	"""

	def judge(self, search_value, judge_value):
		if search_value <=judge_value:
			return True
		else:
			return False


class Equal(Judge):
	"""
	小于等于的业务条件判断
	"""

	def judge(self, search_value, judge_value):
		if search_value ==judge_value:
			return True
		else:
			return False

class Contain(Judge):

	def judge(self,search_value, judge_value):
		if search_value in judge_value:
			return True
		else:
			return False


class NotContain(Judge):
	def judge(self,search_value, judge_value):
		if search_value not in judge_value:
			return True
		else:
			return False


class GetJudgeValue(object):

	def __init__(self):
		self.db = DbOption()


	def get_judge_value(self,judge_value_tuple):
		"""
		如果是sql，就处理下
		:param judge_value_tuple:
		:return:
		"""
		judge_value_tuple = eval(judge_value_tuple)
		if not isinstance(judge_value_tuple,tuple):
			raise JudgeParamsError("judge_value_tuple 必须是tuple 类型")
		judge_type = judge_value_tuple[0]
		if judge_type == "select":
			judge_value = self.db.select(judge_value_tuple[1])[0][0]
			return judge_value
		judge_value = judge_value_tuple[1]
		return judge_value


class JudgeHoler(object):
	"""
	步骤条件判断主方法
	"""
	def start_judge(self,func,*args,**kwargs):
		return func.judge(*args,**kwargs)