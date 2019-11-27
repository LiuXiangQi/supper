# coding:utf-8
from webkeyword.models import UserToken
import logging

def get_user_id(data):
	"""
	user token 验证
	"""
	try:
		token = data.get('user_token' ,False)
		obj = UserToken.objects.filter(token=str(token))
		user_id = obj[0].username_id
		return user_id
	except Exception as e:
		logging.error(e)
		return  False