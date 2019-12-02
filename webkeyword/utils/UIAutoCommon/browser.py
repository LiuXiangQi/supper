# -*- coding: utf-8 -*-

# -----------------*----------------- 
# @Time : 2019-11-28 18:21
# @Author : Dorom
# @Site : 
# @File : browser.py
# @Tag : 启动浏览器操作
# @Version : 
# @Software: PyCharm
# -----------------*----------------- 

from selenium import webdriver
from webkeyword.utils.errorException import BrowserError


class Browser(object):

	def open_broswer(self,browser_type,url,webdriver_path):
		start_open_browser_dict = {
			"Chrome": lambda webdriver_path : webdriver.Chrome(executable_path=webdriver_path),
			"Firefox": lambda webdriver_path : webdriver.Firefox(executable_path=webdriver_path)
		}

		browser = start_open_browser_dict.get(browser_type,False)
		if not browser:
			raise BrowserError
		driver = browser(webdriver_path)
		driver.get(url)
		driver.maximize_window()
		return driver


if __name__ == '__main__':
	b = Browser()
	b.open_broswer("Chrome","https://www.baidu.com","/usr/local/bin/chromedriver")