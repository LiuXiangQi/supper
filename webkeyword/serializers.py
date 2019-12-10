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
from webkeyword.models import User,Project,CaseGroup,Case,CaseProcedure,GlobalData


class UserSerializers(serializers.ModelSerializer):
	"""
	用户信息序列化
	"""
	class Meta:
		model = User
		fields = ('username','password')


class UserDesSerializers(serializers.ModelSerializer):
	"""用户信息反序列化"""
	username = serializers.CharField(max_length=255)
	password = serializers.CharField(max_length=255)
	class Meta:
		model = User
		fields = ('username','password')


class ProjectSerializers(serializers.ModelSerializer):
	"""项目信息序列化"""
	class Meta:
		model = Project
		fields = ('id','name','version','type','description')

	def update(self, instance, validated_data):
		updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
		instance.name = validated_data.get("name",instance.name)
		instance.version = validated_data.get("version",instance.version)
		instance.description = validated_data.get("description",instance.description)
		instance.updateTime = updateTime
		instance.save()
		return instance

	def create(self, validated_data):
		return Project.objects.create(**validated_data)


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
		fields = ('id','groupName','description','projectId','createTime','updateTime')

	def update(self, instance, validated_data):
		# updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%m:%s", required=False, read_only=True)

		instance.projectId = validated_data.get("projectId",instance.projectId)
		instance.groupName = validated_data.get("groupName",instance.groupName)
		instance.description = validated_data.get("description",instance.description)
		instance.createTime = validated_data.get("createTime",instance.createTime)
		instance.updateTime = validated_data.get("updateTime",instance.updateTime)
		instance.save()
		return instance

	def create(self, validated_data):

		return CaseGroup.objects.create(**validated_data)


class CaseSerializers(serializers.ModelSerializer):
	"""
	创建接口序列化
	"""

	class Meta:
		model = Case
		fields = ('id','caseName','datails','caseGroupId')

	def create(self, validated_data):

		return Case.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""

		:param instance:
		:param validated_data:
		:return:
		"""
		instance.caseName = validated_data.get("caseName",instance.caseName)
		instance.datails = validated_data.get("datails",instance.datails)
		instance.caseGroupId = validated_data.get("caseGroupId",instance.caseGroupId)
		instance.save()
		return instance



class CaseProcedureSerializers(serializers.ModelSerializer):
	"""
	添加用例操作步骤接口
	"""
	class Meta:
		model = CaseProcedure
		fields = ("id","caseId","datails","step","KeyWord","element","send_key_value","returnValue","link_step_id",
				  "judge_key_word","judge_step_set","for_step_set")


	def update(self, instance, validated_data):
		"""
		重写update方法
		:param instance:
		:param validated_data:
		:return:
		"""
		instance.caseId = validated_data.get("caseId",instance.caseId)
		instance.datails = validated_data.get("datails",instance.datails)
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


class StartCaseSeriailzers(serializers.Serializer):
	"""
	执行单个测试用例接口序列化
	"""
	# BrowserType_chioce = (
	# 	("Chrome","Chrome"),
	# 	("Firefox","Firefox")
	# )
	destUrl = serializers.CharField(max_length=256,required=True)
	browserType = serializers.CharField(max_length=256,required=True)
	webdriverPath = serializers.CharField(max_length=256,required=True)
	projectId=serializers.IntegerField(required=True)
	caseGroupId = serializers.IntegerField(required=True)
	caseId = serializers.IntegerField(required=True)