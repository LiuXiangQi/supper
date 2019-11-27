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
from webkeyword.models import User,Project,CaseGroup,Case,CaseDatails


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
		updateTime = serializers.DateTimeField(format='%Y-%m-%d %H:%m:%s', required=False, read_only=True)
		instance.name = validated_data.get("name",validated_data.name)
		instance.version = validated_data.get("version",validated_data.version)
		instance.description = validated_data.get("description",validated_data.description)
		instance.updateTime = updateTime
		instance.save()
		return instance

	def create(self, validated_data):
		return Project.objects.create(**validated_data)


class CaseGroupSerializers(serializers.ModelSerializer):
	"""
	用例分组信息 反序列化
	"""
	class Meta:
		model = CaseGroup
		fields = ('id','groupName','description','projectId','createTime','updateTime')

	def update(self, instance, validated_data):
		updateTime = serializers.DateTimeField(format='%Y-%m-%d %H:%m:%s', required=False, read_only=True)
		instance.groupName = validated_data.get("groupName",instance.groupName)
		instance.description = validated_data.get("description",instance.description)
		instance.projectId = validated_data.get("projectId",instance.projectId)
		instance.updateTime = updateTime
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



class CaseDatailsSerializers(serializers.ModelSerializer):
	"""
	添加用例操作步骤接口
	"""
	class Meta:
		model = CaseDatails
		fields = ("id","case_id","datails","seq","Key_word","type","ele","value")


	def update(self, instance, validated_data):
		"""
		重写update方法
		:param instance:
		:param validated_data:
		:return:
		"""
		instance.case_id = validated_data.get("case_id",instance.case_id)
		instance.datails = validated_data.get("datails",instance.datails)
		instance.seq = validated_data.get("seq",instance.seq)
		instance.Key_word = validated_data.get("Key_word",instance.Key_word)
		instance.type = validated_data.get("type",instance.type)
		instance.ele = validated_data.get("ele",instance.ele)
		instance.value = validated_data.get("type",instance.value)
		instance.save()
		return instance

	def create(self, validated_data):
		"""
		重写 create 方法
		:param validated_data:
		:return:
		"""
		return CaseDatails.objects.create(**validated_data)