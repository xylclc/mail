import os
import sys

import pyautogui
from selenium import webdriver
import unittest
from selenium.webdriver.support.select import Select
from time import sleep
import time
import unittest
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains




class Test_Cloud(unittest.TestCase):
    '''邮箱设置模块'''
    driver = None
    hasfile=False

    @classmethod
    def setUpClass(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        driver = webdriver.Chrome(options=opt)
        driver.maximize_window()
        driver.implicitly_wait(30)
        driver.get("http://mail.sic-ca.com/login.jsp")
        driver.find_element_by_id("name").send_keys("auto22")
        driver.find_element_by_id("password").send_keys("a123456_")
        # sleep(3)
        driver.find_element_by_class_name("put_sign").click()
        # 点击登录
        self.driver = driver

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def setUp(self):
        sleep(3)

    def tearDown(self):
        sleep(2)
        if hasattr(self, '_outcome'):
            errors = self._outcome.errors
            for test, exc_info in errors:
                if exc_info:
                    path = os.path.join(os.getcwd(), "pic")
                    self.driver.save_screenshot(os.path.join(path, '%s.png') % self._testMethodName)
        self.driver.refresh()

    #判断元素是否存在的方法
    def isElementExist(self,xpath):
        try:
            self.driver.find_element("xpath",xpath)
            return True
        except:
            return False

    # 上传功能
    def test_01_upload(self):
        driver = self.driver
        # try:
        driver.find_element("xpath","//*[text()='上传文件']").click()
        sleep(1)
        #向上传框输入文件地址
        filepath=os.path.join(os.getcwd(),"test.png")
        driver.find_element("id", "select_btn_1").send_keys(filepath)
        sleep(3)
        driver.refresh()
        #检查上传好的文件的名字
        sleep(3)
        filename=driver.find_element("css selector","#ypIconView dd").text
        self.assertEqual(filename,"test.png")
        Test_Cloud.hasfile=True
        # except Exception as e:
        #     path = os.path.join(os.path.dirname(os.getcwd()), "pic")
        #     driver.save_screenshot(os.path.join(path, '%s.png') % self._testMethodName)

    def test_08_openfile(self):
        if self.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='打开']").click()
        sleep(2)
        # 切换到新页面
        driver.switch_to.window(driver.window_handles[-1])
        # 检查页面标题
        self.assertEqual(driver.title, "查看文件")
        # 检查文件标题
        name = driver.find_element("css selector", ".yp_r_doc_title .ypfile_title").text
        self.assertEqual(name, "test.png")
        # 检查文件大小
        info = driver.find_element("css selector", ".yp_r_info>li:nth-child(4)").text
        # self.assertEqual(info, "大小：80.7KB")
        driver.close()
        # 返回原页面
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)
        # 原页面有此文件，说明返回成功，因为新页面也有相应的文字，所以这边不用文字定位
        filename = driver.find_element("css selector", ".list_c.ypiconitem[isimage='1'] dd").text
        self.assertEqual(filename, "test.png")

if __name__ == '__main__':
    unittest.main(verbosity=2)