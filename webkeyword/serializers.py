# -*- coding: utf-8 -*-

# -----------------*-----------------
# @Time : 2019-11-25 18:12
# @Author : Dorom
# @Site :
# @File : api_case_datails.py
# @Tag : 用例执行步骤接口
# @Version : V1
# @Software: PyCharm
# -----------------*-----------------

from rest_framework import serializers
from webkeyword.models import User,Project,CaseGroup,Case,CaseProcedure,GlobalData,\
	TearDownCase,ApiInfo,CaseGroupHost


class UserSerializers(serializers.Serializer):
	"""
	用户信息序列化
	"""
	username = serializers.CharField(max_length=255)
	password = serializers.CharField(max_length=255)


class ProjectSerializers(serializers.ModelSerializer):
	"""项目信息序列化"""
	class Meta:
		model = Project
		fields = ('id','name','version','type','description')

	def update(self, instance, validated_data):
		instance.name = validated_data.get("name",instance.name)
		instance.version = validated_data.get("version",instance.version)
		instance.description = validated_data.get("description",instance.description)
		instance.updateTime = validated_data.get("updateTime", instance.updateTime)
		instance.save()
		return instance

	def create(self, validated_data):
		return Project.objects.create(**validated_data)

class DesProjectSerializers(serializers.ModelSerializer):
	"""项目信息序列化"""
	class Meta:
		model = Project
		fields = ('id','name','version','type','description','createTime','updateTime')



class GlobalParamsSerializers(serializers.ModelSerializer):
	"""
	全局变量添加接口序列化
	"""

	class Meta:
		model = GlobalData
		fields = ("id","name","description","params")

	def update(self, instance, validated_data):
		instance.name = validated_data.get("name",instance.name)
		instance.description = validated_data.get('description',instance.description)
		instance.params = validated_data.get('params',instance.params)
		instance.save()
		return instance

	def create(self, validated_data):
		return GlobalData.objects.create(**validated_data)


class CaseGroupSerializers(serializers.ModelSerializer):
	"""
	用例分组信息 反序列化
	"""
	class Meta:
		model = CaseGroup
		fields = ('id','groupName','description','projectId')

	def update(self, instance, validated_data):

		instance.projectId = validated_data.get("projectId",instance.projectId)
		instance.groupName = validated_data.get("groupName",instance.groupName)
		instance.description = validated_data.get("description",instance.description)
		instance.updateTime = validated_data.get("updateTime",instance.updateTime)
		instance.save()
		return instance

	def create(self, validated_data):

		return CaseGroup.objects.create(**validated_data)


class DesCaseGroupSerializers(serializers.ModelSerializer):
	"""
	用例分组信息 序列化
	"""
	class Meta:
		model = CaseGroup
		fields = ('id','groupName','description','projectId','createTime','updateTime')


class CaseSerializers(serializers.ModelSerializer):
	"""
	创建接口序列化
	"""

	class Meta:
		model = Case
		fields = ('id','caseName','description','caseGroupId')

	def create(self, validated_data):

		return Case.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""

		:param instance:
		:param validated_data:
		:return:
		"""
		instance.caseName = validated_data.get("caseName",instance.caseName)
		instance.description = validated_data.get("description",instance.description)
		instance.caseGroupId = validated_data.get("caseGroupId",instance.caseGroupId)
		instance.save()
		return instance


class CaseProcedureSerializers(serializers.ModelSerializer):
	"""
	添加用例操作步骤接口
	"""
	class Meta:
		model = CaseProcedure
		fields = ("id","caseId","description","step","KeyWord","element","send_key_value","link_step_id",
				  "judge_key_word","judge_step_set","for_step_set")

	def update(self, instance, validated_data):
		"""
		重写update方法
		:param instance:
		:param validated_data:
		:return:
		"""
		instance.caseId = validated_data.get("caseId",instance.caseId)
		instance.description = validated_data.get("description",instance.description)
		instance.step = validated_data.get("step",instance.step)
		instance.KeyWord = validated_data.get("KeyWord",instance.KeyWord)
		instance.element = validated_data.get("element",instance.element)
		instance.send_key_value = validated_data.get("send_key_value",instance.send_key_value)
		instance.link_step_id = validated_data.get("link_step_id",instance.link_step_id)
		instance.judge_key_word = validated_data.get("judge_key_word",instance.judge_word)
		instance.judge_value = validated_data.get("judge_value",instance.judge_value)
		instance.judge_step_set = validated_data.get("judge_step_set",instance.judge_step_set)
		instance.for_step_set = validated_data.get("for_step_set",instance.for_step_set)
		instance.save()
		return instance

	def create(self, validated_data):
		"""
		重写 create 方法
		:param validated_data:
		:return:
		"""
		return CaseProcedure.objects.create(**validated_data)


class TearDownCaseSerializer(serializers.ModelSerializer):
	"""
	用例sql 数据清理
	"""

	class Meta:
		model = TearDownCase
		fields = ('caseId','groupId','sql_text_li')

	def update(self, instance, validated_data):
		"""
		重写update 方法
		:param instance:
		:param validated_data:
		:return:
		"""
		instance.caseId = validated_data.get('caseId',instance.caseId)
		instance.groupId = validated_data.get('groupId',instance.groupId)
		instance.sql_text = validated_data.get('sql_text',instance.sql_text)
		instance.save()
		return instance

	def create(self, validated_data):
		"""
		重写create 方法
		:param validated_data:
		:return:
		"""
		return TearDownCase.objests.create(**validated_data)


class StartCaseSerializers(serializers.Serializer):
	"""
	执行单个测试用例接口序列化
	"""
	LOGIN = (('true',True),
			('false',False))

	destUrl = serializers.CharField(max_length=256,required=True)
	browserType = serializers.CharField(max_length=256,required=True)
	webdriverPath = serializers.CharField(max_length=256,required=True)
	projectId=serializers.IntegerField(required=True)
	caseGroupId = serializers.IntegerField(required=True)
	login= serializers.ChoiceField(choices=LOGIN)   # 是否需要登录
	caseId = serializers.IntegerField(required=True)


class CaseGroupHostSerializer(serializers.ModelSerializer):
	"""
	添加host序列化
	"""
	class Meta:
		model = CaseGroupHost
		fields = ('caseGroupId','hostName','host')

	def update(self, instance, validated_data):
		instance.caseGroupId = validated_data.get('caseGroupId',instance.caseGroupId)
		instance.hostName = validated_data.get('hostName',instance.hostName)
		instance.host = validated_data.get('host',instance.host)
		instance.save()
		return instance

	def create(self, validated_data):

		return  CaseGroupHost.objects.create(**validated_data)


class AddInterfaceApiSerializer(serializers.ModelSerializer):
	"""
	添加接口
	"""
	headers = serializers.JSONField()
	requestparams = serializers.JSONField()

	class Meta:
		model = ApiInfo
		fields = ('caseId','seqId','httpType','name','path','model','paramsType','headers',
				  'requestparams')  # apiparams


class UpdateInterfaceSerializer(serializers.Serializer):
	httpTypes = (
		('Http','Http'),
		('Https','Https')
	)
	models_types = (
		('get', "get"),
		('post', 'post'),
		('patch', 'patch'),
		('put', 'put'),
		('delete', 'delete')
	)
	params_types = (
		('raw', 'raw'),
		('params', 'params')
	)

	httpType = serializers.ChoiceField(choices=httpTypes,default='Http',read_only=True)
	name = serializers.CharField(max_length=128,allow_blank=True,allow_null=True,read_only=True)
	path = serializers.CharField(max_length=512,allow_blank=True,allow_null=True,read_only=True)
	model = serializers.ChoiceField(choices=models_types,read_only=True)
	paramsType = serializers.ChoiceField(choices=params_types,read_only=True)
	headers = serializers.JSONField()
	requestparams = serializers.JSONField()


