# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-12 19:45
# @Author : Dorom
# @File : api_tear_down_case.py
# @Tag :  清理用例数据接口
# @Software: PyCharm
# -----------------*----------------- 

from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from webkeyword.utils.api_response import JsonResponse
from webkeyword.models import TearDownCase,Case,CaseGroup
from webkeyword.serializers import TearDownCaseSerializer
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import re


class TearDownCaseAddApi(APIView):

    def check_params(self,data):
        caseId = data.get('caseId',False)
        groupId = data.get('groupId',False)
        try:
            Case.objects.get(id=caseId)
        except:
            res = "caseId:{0} not found ".format(caseId)
            return JsonResponse(code=status.HTTP_404_NOT_FOUND,data={"res":res},msg='fail')
        try:
            CaseGroup.objects.get(id=groupId)
        except:
            res = "groupId:{0} not found ".format(groupId)
            return JsonResponse(code=status.HTTP_404_NOT_FOUND,data = {'res':res} ,msg='fail')

    def check_sql_text(self,data):
        """
        插入的sql 语句检查是否有加限制条件
        :param data:
        :return:
        """
        sql_text_li = data.get('sql_text_li',False)
        delete_patterm = re.compile(r'delete from (.*)')
        update_patterm = re.compile(r'update (.*)')
        if sql_text_li:
            sql_text_li = eval(sql_text_li)
            for sql_text in sql_text_li:
                delete_res = delete_patterm.findall(sql_text)
                if delete_res:
                    delete_res_patterm = re.compile('where')
                    res = delete_res_patterm.findall(delete_res[0])
                    if not res:
                        result = "The delete statement must be conditional."  # 删除语句必出加上限制条件
                        return JsonResponse(code=status.HTTP_404_NOT_FOUND,data = {'res':result},msg = 'fail' )
                else:
                    update_res = update_patterm.findall(sql_text)
                    if update_res:
                        update_res_patterm = re.compile('where')
                        res = update_res_patterm.findall(update_res[0])
                        if not res:
                            result = "The update statement must be conditional."  # update 语句必须加上现在条件
                            return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={'res': result}, msg='fail')

    def post(self,request):
        data = request.data
        res = self.check_params(data)
        if res:
            return res
        sql_res = self.check_sql_text(data)
        if sql_res:
            return sql_res
        serializer = TearDownCaseSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg="seccuss")
        return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=serializer.errors,msg="fail")


class TearDownCaseApi(APIView):

    def check_pk(self,pk):
        queryset = TearDownCase.objects.filter(pk = pk)
        return queryset

    def get(self,request,pk):

        queryset = self.check_pk(pk)
        if not queryset:
            res = "pk: {0} not found".format(pk)
            return JsonResponse(code=status.HTTP_404_NOT_FOUND,data={"res":res},msg="fail")
        # try:
        #     page_size = request.GET.get('page_size',20)
        #     page_size = int(page_size)
        # except Exception as e:
        #     return JsonResponse(code=status.HTTP_404_NOT_FOUND,data={'res':e},msg='fail')
        serializer = TearDownCaseSerializer(data=queryset)
        return JsonResponse(code=status.HTTP_200_OK,data=serializer.data,msg='seccuss')

    def put(self,request,pk):
        data = request.data
        queryset = self.check_pk(pk)
        if not  queryset:
            res = "pk: {0} not found".format(pk)
            return JsonResponse(code = status.HTTP_404_NOT_FOUND, data = {"res": res}, msg = "fail")
        serializer = TearDownCaseSerializer(pk = pk,data = data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(code = status.HTTP_200_OK,data =serializer.data,msg = 'seccuss')
        return JsonResponse(code = status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request,pk):
        queryset = self.check_pk(pk)
        if not queryset:
            res = "pk: {0} not found".format(pk)
            return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={"res": res}, msg="fail")
        with transaction.atomic():
            queryset.dalete()
            return JsonResponse(code=status.HTTP_200_OK, data= {}, msg='seccuss')