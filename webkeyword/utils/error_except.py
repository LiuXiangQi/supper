# coding:utf-8

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
