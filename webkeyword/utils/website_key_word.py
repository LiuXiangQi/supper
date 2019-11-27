# coding:utf-8

from selenium.webdriver.support.ui import WebDriverWait
from webkeyword.utils.error_except import EleNOtFound
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time,os

class BaseView(object):

	def __init__(self,driver):
		self.driver=driver

	def find_element(self,loc,timeout=5):
		if self.check_element(loc,timeout):
			return self.driver.find_element(*loc)
		else:
			self.get_screenshot_imge()
			raise EleNOtFound("{0} 元素未找到异常".format(loc))

	def Select(self, loc):
		"""Select 下拉框"""
		s = Select(self.find_element(loc))
		return s

	def get_screenshot_imge(self):
		tm = time.strftime("%Y-%m-%d",time.localtime(time.time()))
		file_dir = os.path.join("D:\workspace\website\img",tm)
		if not os.path.exists(file_dir):
			os.mkdir(file_dir)
		tim = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
		file_path = os.path.join(file_dir,tim+".png")
		self.driver.get_screenshot_as_file(file_path)

	def find_elements(self,loc,timeout=5):
		if self.check_elements(loc,timeout):
			return self.driver.find_elements(*loc)
		else:
			raise EleNOtFound("{0} 元素列表未找到".format(loc))

	def find_element_Uiautomator(self,loc):
		""" 使用uiuatomator定位元素"""

		return self.driver.find_element_by_android_uiautomator\
			('new UiSelector().{0}(\"{1}\")'.format(loc[0],loc[1]))

	def find_accessiblity(self,loc,timeout=10):
		"""accessibility Android 使用的是 content-desc
		属性 IOS使用的是 accessibility identifier属性"""
		if self.check_accessiblity(loc,timeout):
			ele = self.driver.find_element_by_accessibility_id(loc)
			return ele
		else:
			raise EleNOtFound()

	def ios_predicates(self,ele,timeout =5):
		"""查找多个元素"""
		if self.ios_check_elements(ele,timeout):
			ele = self.driver.find_elements_by_ios_predicate(ele)
			return ele
		else:
			raise EleNOtFound("iOS ios_predicates：{} 元素未找到".format(ele))

	def ios_predicate(self,ele,timeout=5):
		"""查找单个元素"""
		if self.ios_check_element(ele, timeout):
			ele = self.driver.find_element_by_ios_predicate(ele)
			return ele
		else:
			raise EleNOtFound("iOS ios_predicate：{} 元素未找到".format(ele))

	def check_element(self,loc,time=10):
		try:
			WebDriverWait(self.driver,time).until(lambda x:x.find_element(*loc))
			return True
		except:
			return False

	def check_elements(self,loc,time=10):
		try:
			WebDriverWait(self.driver,time).until(lambda x:x.find_elements(*loc))
			return True
		except:
			return False

	def ios_check_element(self,ele,timeout=10):
		try:
			WebDriverWait(self.driver,timeout).until(lambda x:x.find_element_by_ios_predicate(ele))
			return True
		except:
			return False

	def ios_check_elements(self,ele,timeout=10):
		try:
			WebDriverWait(self.driver,timeout).until(lambda x:x.find_element_by_ios_predicate(ele))
			return True
		except:
			return False

	def check_accessiblity(self,loc,timeout=10):
		try:
			WebDriverWait(self.driver,timeout).until(lambda x:x.find_element_by_accessibility_id(loc))
			return True
		except:
			return False


	def click(self,loc):
		self.find_element(loc).click()

	def get_text(self,loc):
		textData = self.find_element(loc).text
		return textData

	def set_value(self,ele,params):
		"""ios 输入值"""
		self.ios_predicate(ele).set_value(params)

	def send_keys(self,loc,text):
		ele = self.find_element (loc)
		ele.clear()
		ele.send_keys (text)

	def get_source_page(self):
		"""获取当前页面源码"""
		return  self.driver.page_source

	def swatch_to_context(self,context=None):
		contexts_list = self.get_context_list()
		context = self.driver.current_context
		for i in contexts_list:
			if i != context:
				self.driver.switch_to.context(i)
				break

	def get_context_list(self):
		"""获取窗口列表"""
		return self.driver.contexts

	def get_current(self):
		"""获取当前窗口"""
		return self.driver.current_context

	def choice_context(self,context):
		"""选择窗口切换"""
		self.driver._switch_to.context(context)

	def website_swatch_to(self):
		"""切换窗口句柄"""
		all_heandles = self.driver.window_handles
		for heandle in all_heandles:
			if heandle != self.driver.current_window_handle:
				self.driver._switch_to.window(heandle)

	def switch_to_frame(self,loc):
		"""frame 窗口切换"""
		self.driver.switch_to.frame(loc)

	def switch_to_default(self):
		"""selenium 切换回主页窗口"""
		self.driver.switch_to.default_content()

	def back(self):
		self.driver.keyevent(4)

	def refresh(self):
		"""刷新网页"""
		self.driver.refresh()

	def opterion_keycode(self,keycode,metastate=None):
		self.driver.press_keycode(keycode,metastate)


	def get_window_size(self):
		return self.driver.get_window_size()

	def swipe(self,start_x, start_y, end_x, end_y, duration):
		return self.driver.swipe(start_x, start_y, end_x, end_y, duration)


	def checked(self,loc):
		ele = self.find_element(loc)
		is_checked = ele.get_attribute("clickable")
		if is_checked == "false":
			return 0
		else:
			return is_checked

	def checked_clickable(self,loc):
		ele = self.find_element(loc)
		is_checked = ele.get_attribute("clickable")
		if is_checked == "false":
			return 0
		else:
			return is_checked

	def tap(self,x,y,time=500):
		"""
		点击操作
		:param x:
		:param y:
		:param time:
		:return:
		"""
		are = self.get_window_size()

		x1 = int((float(x)/are["width"])*are["width"])
		y1 = int((float(y/are["height"]))*are["height"])
		self.driver.tap([(x1,y1),(x1,y1)],time)


	def get_page(self):
		# self.driver.page_source

		return self.driver.page_source

	def get_size(self):
		x = self.get_window_size()['width']
		y = self.get_window_size()['height']
		return x,y

	def swipeUp(self,x_num=0.5,y1_num=0.1,y2_num=0.5,time=500):
		are = self.get_size()
		x = int(are[0]*x_num)
		y1 = int(are[1]*y1_num)
		y2 = int(are[1]*y2_num)
		self.swipe(x,y1,x,y2,time)

	def swipeDown(self,x_num=0.5,y1_num=0.1,y2_num=0.5,time=500):
		are = self.get_size()
		x = int(are[0]*x_num)
		y1 = int(are[1]*y1_num)
		y2 = int(are[1]*y2_num)
		self.swipe(x,y2,x,y1,time)

	def swipeRight(self,time=500):
		are = self.get_size()
		x1 = int(are[0]*0.1)
		x2 = int(are[0]*0.9)
		y = int(are[1]*0.5)
		self.swipe(x1,y,x2,y,time)

	def swipeLeft(self,x_num=0.1,y1_num=0.5,x2_num=0.9,time=500):

		are = self.get_size()
		x1 = int(are[0]*x_num)
		x2 = int(are[0]*x2_num)
		y = int(are[1]*y1_num)
		self.swipe(x2,y,x1,y,time)


	def moveTo(self,loc):
		"""鼠标移动到元素ele"""
		ele = self.find_element(loc)
		ActionChains(self.driver).move_to_element(ele).perform()

	def js_move(self,num=1000):
		""" 调用js 拖拽"""
		js = "var q=document.documentElement.scrollTop={0}".format(num)
		self.driver.execute_script(js)