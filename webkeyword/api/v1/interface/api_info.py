# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-24 16:44
# @Author : Dorom
# @File : api_info.py
# @Tag : 
# @Software: PyCharm
# -----------------*-----------------

from django.db import transaction
from django.forms.models import model_to_dict
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from rest_framework import status
from rest_framework.views import APIView

from webkeyword.serializers import AddInterfaceApiSerializer,UpdateInterfaceSerializer
from webkeyword.utils.api_response import JsonResponse
from webkeyword.models import Case,ApiInfo,ApiParams,ApiHeaders
from webkeyword.utils.logger import logger
import time

def check_caseId(caseId):
    try:
        Case.objects.get(id=caseId)
    except:
        data = {'res': 'caseId 不存在'}
        return JsonResponse(code=status.HTTP_502_BAD_GATEWAY, data=data, msg='fail')


def check_seq( caseId, seqId):
    queryset = ApiInfo.objects.filter(caseId=caseId, seqId=seqId)
    if queryset:
        data = {'res': '用例步骤已存在'}
        return JsonResponse(code=status.HTTP_502_BAD_GATEWAY, data=data, msg='fail')


def get_check_seq(caseId,seqId):
    """
    获取用例接口的数据
    :param caseId:
    :param seqId:
    :return:
    """
    queryset = ApiInfo.objects.filter(caseId=caseId, seqId=seqId)
    if not queryset:
        data = {'res': '用例步骤不存在'}
        return JsonResponse(code=status.HTTP_502_BAD_GATEWAY, data=data, msg='fail')


def get_apiinfo_data(caseId,seqId=None):

    caseId_res = check_caseId(caseId)
    if caseId_res:
        return caseId_res
    if seqId is not None:
        seq_res = get_check_seq(caseId,seqId)
        if seq_res:
            return seq_res

    apiinfo_queryset = ApiInfo.objects.filter(caseId=caseId,seqId=seqId)
    headers_queryset = ApiHeaders.objects.filter(caseId=caseId,seqId=seqId)
    params_queryset = ApiParams.objects.filter(caseId=caseId,seqId=seqId)

    api_info = model_to_dict(apiinfo_queryset[0])
    if not headers_queryset:
        headers = {}
    else:
        headers = model_to_dict(headers_queryset[0])
    if not params_queryset:
        params = []
    else:
        params = []
        for param_queryset in params_queryset:
            params.append(model_to_dict(param_queryset))
    data = {"apiinfo":api_info,"headers":headers,"params":params}
    return JsonResponse(code=status.HTTP_200_OK,data=data,msg='seccuss')


class ApiInfoView(APIView):

    def post(self,request):
        """
        添加测试url信息接口
        :param request: headers、requestparams 必须为字典类型
        :return:
        """
        data = request.data
        serializers = AddInterfaceApiSerializer(data=data)
        with transaction.atomic():
            if serializers.is_valid():
                try:
                    caseId = data.get('caseId')
                    seqId = data.get('seqId')

                    caseId_res = check_caseId(caseId)
                    if caseId_res:
                        return caseId_res
                    seq_res = check_seq(caseId,seqId)
                    if seq_res:
                        return seq_res

                    caseId, seqId, httpType, name, path, model, paramsType,headers, requestparams = [params for params in
                                                                                             data.values()]
                    if not isinstance(headers,dict) or not isinstance(requestparams,dict):
                        data = {'res':'requestparams or headers  object has no attribute items'}
                        return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data=data,msg='fail')
                    create_time = str(time.time())[:10]
                    # 添加APIInfo基础信息
                    ApiInfo.objects.create(caseId=caseId,seqId=seqId,httpType=httpType,name=name,
                                           path=path,model=model,paramsType=paramsType,createTime=create_time,updateTime=create_time)

                    # 添加接口请求头
                    for name,value in headers.items():
                        ApiHeaders.objects.create(caseId=caseId,seqId=seqId,name=name,value=value)

                    # 添加接口参数
                    for name,value in requestparams.items():
                        ApiParams.objects.create(caseId=caseId,seqId=seqId,name=name,value=value)

                    return JsonResponse(code=status.HTTP_200_OK, data=data, msg="success")
                except Exception as e :
                    res = str(e)
                    return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'res':res}, msg='fail')
            return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializers.errors, msg='fail')

    def get(self,request):
        """
        获取所有的用例接口信息
        :param request:
        :return:
        """

        caseId = request.GET.get('caseId',False)
        if not caseId:
            return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={'res': 'caseId not found'}, msg="fail")

        res = get_apiinfo_data(caseId)
        return res



class OpertionApiInfoView(APIView):

    def get(self,request,caseId,seqId):
        """
        获取单个用例接口数据
        :param request:
        :param caseId:
        :param seqId:
        :return:
        """
        if not caseId:
            return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={'res': 'caseId not found'}, msg="fail")
        if not seqId:
            return JsonResponse(code=status.HTTP_404_NOT_FOUND, data={'res': 'seqId not found'}, msg="fail")
        res = get_apiinfo_data(caseId,seqId)
        return res

    def delete(self,request,caseId,seqId):
        """
        删除用例的接口
        :param request:
        :param caseId:
        :param seqId:
        :return:
        """

        caseId_res = check_caseId(caseId)
        if caseId_res:
            return caseId_res
        seqId_res = get_check_seq(caseId, seqId)
        if seqId_res:
            return seqId_res
        try:
            with transaction.atomic():
                ApiInfo.objects.filter(caseId=caseId, seqId=seqId).delete()
                ApiHeaders.objects.filter(caseId=caseId, seqId=seqId).delete()
                ApiParams.objects.filter(caseId=caseId, seqId=seqId).delete()
                return JsonResponse(code=status.HTTP_200_OK, msg='seccuss')
        except Exception as e:
            return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data={'res':str(e)},msg='fail')

    def put(self,request,caseId,seqId):
        """
        修改单个用例接口数据
        :param request:
        :param caseId:
        :param seqId:
        :return:
        """
        data = request.data
        serializers = UpdateInterfaceSerializer(data = data)
        if serializers.is_valid():
            caseId_res = check_caseId(caseId)
            if caseId_res:
                return caseId_res
            seqId_res = get_check_seq(caseId,seqId)
            if seqId_res:
                return seqId_res

            httpType, name, path, model, paramsType, headers, requestparams = [params for params in data.values()]

            if not isinstance(headers, dict) or not isinstance(requestparams, dict):
                data = {'res': 'requestparams or headers  object has no attribute items'}
                return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data, msg='fail')

            with transaction.atomic():
                update_time = str(time.time())[:10]

                ApiInfo.objects.filter(caseId=caseId,seqId=seqId).update(httpType=httpType,name=name,
                                                                         path=path,paramsType=paramsType,updateTime=update_time)

                # 更新headers
                self.update_headers(caseId,seqId,headers)

                # 更新params
                self.update_params(caseId,seqId,requestparams)

            return JsonResponse(code=status.HTTP_200_OK,msg='seccuss')
        return JsonResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,data= serializers.errors,msg='fail')

    def update_headers(self,caseId,seqId,headers):
        """
        更新header 数据
        :param caseId:
        :param seqId:
        :param headers:
        :return:
        """
        # 传入的更新headers数据，如果 name 存在就更新，不存在就新建
        header_list = []
        for name, value in headers.items():
            defaults = {}
            defaults['caseId'] = caseId
            defaults['seqId'] = seqId
            defaults['name'] = name
            header_list.append(name)
            ApiHeaders.objects.update_or_create(defaults=defaults, value=value)

        # 删除更新headers 数据后多余，不需要用的header 数据
        headersqueryset = ApiHeaders.objects.filter(caseId=caseId, seqId=seqId)
        headers_dest_list = []
        for queryset in headersqueryset:
            name = queryset.name
            headers_dest_list.append(name)
        diff_header_list = list(set(headers_dest_list).difference(set(header_list)))
        for name in diff_header_list:
            ApiHeaders.objects.filter(caseId=caseId, seqId=seqId, name=name).delete()

    def update_params(self,caseId,seqId,requestparams):
        """
        更新params 数据
        :param caseId:
        :param seqId:
        :param requestparams:
        :return:
        """
        params_list = []
        for name,value in requestparams.items():
            defaults = {}
            defaults['caseId'] = caseId
            defaults['seqId'] = seqId
            defaults['name'] = name
            params_list.append(name)
            ApiParams.objects.update_or_create(defaults=defaults, value=value)

        paramssqueryset = ApiParams.objects.filter(caseId=caseId, seqId=seqId)

        params_dest_list = []

        for queryset in paramssqueryset:
            name = queryset.name
            params_dest_list.append(name)
        diff_params_list = list(set(params_dest_list).difference(set(params_list)))
        # logger.info(str(diff_params_list))
        for name in diff_params_list:
            ApiParams.objects.filter(caseId=caseId, seqId=seqId, name=name).delete()