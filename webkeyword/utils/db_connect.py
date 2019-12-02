# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-28 17:06
# @Author : Dorom
# @Site : 
# @File : db_connect.py
# @Tag : 
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 


import pymysql
import logging

class DbOption(object):
    def __init__(self):
        # self.cf = read_yaml(DBCONFIG)
        self.host = "120.78.249.137"
        self.username = "developer"
        self.password = "developer123456"
        self.port = 3306
        self.basename = "db_test_api"
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host,user=self.username,passwd=self.password,db=self.basename,port=self.port,charset='utf8')

        except Exception as msg:
            logging.info("数据库连接错误：{0}".format(msg))
        return self.conn

    def reconnect(self):
        """
        数据库重连机制
        :return:
        """
        try:
            self.conn.ping()
            return False
        except:
            return self.connect()

    def select(self,sql):
        cursor  = self.connect().cursor()
        try:
            reconnect = self.reconnect()
            if reconnect:
                cursor = reconnect.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as msg:
            logging.info("sql查询错误：{0}".format(msg)+"\n" + "错误sql:{0}".format(sql))
            data = ()
        cursor.close()
        self.conn.close()
        return data

    def operation(self,sql):
        cursor = self.connect().cursor()
        try:
            reconnect = self.reconnect()
            if reconnect:
                cursor = reconnect.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except Exception as msg:
            self.conn.rollback()
            logging.info("sql:{0} 操作失败：{1}".format(msg,sql))
        cursor.close()
        self.conn.close()