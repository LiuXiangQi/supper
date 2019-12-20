# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-12-17 15:58
# @Author : Dorom
# @File : login.py
# @Tag : 
# @Software: PyCharm
# -----------------*----------------- 

from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')
