# coding:utf-8


from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from webkeyword.utils.api_response import JsonResponse
from webkeyword.serializers import UserSerializers,UserDesSerializers
from webkeyword.models import User,UserToken
import time


class AuthUser(APIView):

	def parameter_check(self,data):
		user_name = data.get('username',False)
		password = data.get('password',False)
		if not user_name or not password:
			return JsonResponse(code='201',msg='账号密码错误')
		else:
			if not isinstance(user_name,str) or not isinstance(password,str):
				return JsonResponse(code=201,msg='登录失败',data='username,password must be str')

	def post(self,request):
		"""用户登录"""
		data = JSONParser().parse(request)
		result = self.parameter_check(data)
		if result:
			return result
		try:
			user_serializer = UserDesSerializers(data=data)
			if user_serializer.is_valid():
				username = data.get('username', False)
				password = data.get('password', False)
				obj = User.objects.filter(username=username, password=password).first()
				user_id = obj.id
				if not obj:
					return JsonResponse(code=201,msg='账号密码错误')
				# 里为了简单，应该是进行加密，再加上其他参数
				token = str(time.time()) + username
				obj_token = UserToken.objects.update_or_create(username=obj, defaults={'token': token})
				res = {"userId":user_id}
				return JsonResponse(code=200,msg='登录成功',data=res)
			else:
				return JsonResponse(code=201,msg=user_serializer.errors)
		except Exception as e:
			print(e)
			return JsonResponse(code=201,msg='参数有误')

