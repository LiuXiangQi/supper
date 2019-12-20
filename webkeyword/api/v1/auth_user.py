# coding:utf-8


from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from webkeyword.utils.api_response import JsonResponse
from webkeyword.serializers import UserSerializers
from webkeyword.models import User,UserToken
import time


class AuthUser(APIView):

	def parameter_check(self,data):
		user_name = data.get('username',False)
		password = data.get('password',False)
		if not user_name or not password:
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data={'res':"账号密码错误"},msg='fail')
		else:
			if not isinstance(user_name,str) or not isinstance(password,str):
				return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data={'res':'username,password must be str'},msg='fail',)

	def post(self,request):
		"""用户登录"""
		data = request.data
		result = self.parameter_check(data)
		if result:
			return result
		try:
			user_serializer = UserSerializers(data=data)
			if user_serializer.is_valid():
				username = data.get('username', False)
				password = data.get('password', False)
				obj = User.objects.filter(username=username, password=password).first()
				if obj:
					user_id = obj.id
					# 里为了简单，应该是进行加密，再加上其他参数
					token = str(time.time()) + username
					UserToken.objects.update_or_create(username=obj, defaults={'token': token})
					token_queryset = UserToken.objects.filter(username=user_id).first()
					res = {"userId":user_id,"UserToken":"{0}".format(token_queryset.token)}
					return JsonResponse(code=status.HTTP_200_OK,msg='seccuss',data=res)
				else:
					return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fila',data={"res":"账号或密码不存在"})
			else:
				return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,msg='fail',data = user_serializer.errors)
		except Exception as e:
			res = {"res": "{0}".format(e)}
			return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=res ,msg='参数有误')