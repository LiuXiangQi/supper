# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-06 16:36
# @Author : Dorom
# @Site : 
# @File : check_result.py
# @Tag : 
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 

import abc


class CheckReport(metaclass=abc.ABCMeta):

	def check_report(self,*args,**kwargs):
		pass