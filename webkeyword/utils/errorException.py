# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-28 17:01
# @Author : Dorom
# @Site : 
# @File : errorException.py
# @Tag : 
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 

class JudgeParamsError(Exception):
	"""
	用例步骤，添加条件判断必须是tuple
	"""
	pass

class EleNOtFound(Exception):
	pass

class FilePathNotFound(Exception):
	"""找不到文件路径"""
	pass

class BrowserError(Exception):
	"""驱动错误"""
	pass

class KeyError(Exception):
	"""值错误"""
	pass


class AttributeError(Exception):
	"""
	获取元素属性值错误
	"""
	pass