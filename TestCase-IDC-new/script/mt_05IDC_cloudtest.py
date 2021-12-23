import os

from selenium import webdriver
from time import sleep
import unittest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class Test_Cloud(unittest.TestCase):
    '''邮箱设置模块'''
    driver = None
    hasfile=False
    hasfolder=False

    @classmethod
    def setUpClass(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")            #del
        driver = webdriver.Chrome(options=opt)
        #driver.maximize_window()
        driver.set_window_size(1920, 1080)           #del
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

    def skip_dependon(depend=""):
        """
        :param depend: 依赖的用例函数名，默认为空
        :return: wraper_func
        """


    # 上传功能
    def test_01_upload(self):
        driver = self.driver
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
        Test_Cloud.hasfile = True
        # except Exception as e:
        #     path = os.path.join(os.path.dirname(os.getcwd()), "pic")
        #     driver.save_screenshot(os.path.join(path, '%s.png') % self._testMethodName)

    # 新建文件夹
    def test_02_newfolder(self):
        driver = self.driver
        driver.find_element("xpath", "//span[text()='新建文件夹']").click()
        sleep(1)
        #输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("ctest")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        # 检查文件夹名字
        filename = driver.find_element("css selector", ".list_c.ypiconitem dd").text
        self.assertEqual(filename, "ctest")
        Test_Cloud.hasfolder=True

    #打开文件夹

    def test_03_openfolder(self):
        driver = self.driver
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='打开']").click()
        sleep(2)
        #检查上方路径中最后一个元素的内容
        spanname=driver.find_elements("css selector","a[rh='open,upload,createFolder']")[1].text
        #如果是ctest，说明进入到了文件夹内部
        self.assertEqual(spanname, "ctest")

    # 分享文件夹
    def test_04_sharefolder(self):
        driver = self.driver
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        #进入分享弹框,中间输入名字，点击搜索
        driver.find_element("id","serachid").send_keys("崔丽丽")
        driver.find_element("id","sousuoid").click()
        sleep(1)
        #中间小搜索框的搜索按钮
        driver.find_element("css selector",".tree-checkbox.tree-checkbox0").click()
        sleep(1)
        #用js把滚动条拉到最下面
        js="document.getElementById('ypBtnPopWin_share').scrollTop = 100000"
        driver.execute_script(js)
        driver.find_element("xpath", "//*[text()='立即分享']").click()
        sleep(3)
        #进入我的分享页面
        driver.find_element("xpath", "//span[contains(text(),'我的分享')]").click()
        sleep(2)
        #比对文件夹名一样说明分享成功
        name= driver.find_element("css selector",".iconUl dd").text
        self.assertEqual(name, "ctest")

         # 刷新页面，开始裢接分享
        driver.refresh()
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        #进入裢接分享标签
        driver.find_element("css selector",".share_links").click()
        #点击分享裢接
        driver.find_element("xpath","//*[@ctype='save']").click()
        #点击复制裢接
        driver.find_element("xpath", "//*[@ctype='copy']").click()
        sleep(1)
        #判断提示复制成功
        txt=driver.find_element("id","infoPopDiv").text
        self.assertEqual(txt,"复制成功")

        #刷新页面，开始邮件分享
        driver.refresh()
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        # 进入发到邮箱标签
        driver.find_element("css selector", ".send_mail").click()
        # 点击邮件分享按钮
        driver.find_element("xpath", "//*[@ctype='sendMail']").click()
        sleep(1)
        #跳到发件页面，切换frame
        driver.switch_to.frame(driver.find_element("css selector",".ke-edit-iframe"))
        #判断发件内容有相关字样
        s=driver.find_element("css selector", ".ke-content").text
        self.assertEqual(s,"您的朋友和您分享了文件：ctest 请点击文件名查看")

    #重命名文件夹
    def test_05_renamefolder(self):
        if Test_Cloud.hasfolder == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(3)
        driver.find_element("xpath", "//span[text()='重命名']").click()
        sleep(2)
        # 输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("ctest1")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        # 检查文件夹名字
        filename = driver.find_element("css selector", ".list_c.ypiconitem dd").text
        self.assertEqual(filename, "ctest1")
        #检查之前的名字不存在了
        result = self.isElementExist("//*[text()='ctest']")
        self.assertFalse(result)

    #复制文件夹
    def test_06_copyfolder(self):
        if Test_Cloud.hasfolder == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        # 新建一个copy文件夹来完成这项功能
        driver.find_element("xpath", "//span[text()='新建文件夹']").click()
        sleep(1)
        # 输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("copy")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        # 把copy复制到ctest1里面
        driver.find_element("xpath", "//dd[text() = 'copy']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='复制到']").click()
        sleep(2)
        # 选中ctest1前面的小框
        driver.find_element("xpath", "//span[text()='ctest1']//preceding-sibling::span[1]").click()
        # 确定按钮
        driver.find_element('css selector', "#ypPopDirTreeWin .dialog-button a.l-btn .icon-ok").click()
        sleep(1)
        # 捕捉复制成功的提示，如果没有提示会报错，提示元素未找到
        driver.find_element("xpath", "//*[text()='复制成功']")
        sleep(3)
        # 判断复制成功后当前目录下还有copy文件夹
        result = self.isElementExist("//dd[text() = 'copy']")
        self.assertTrue(result)
        # 打开ctest1，判断复制成功后copy在里面
        driver.find_element("xpath", "//*[text()='ctest1']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='打开']").click()
        sleep(2)
        # 比对文件夹名称为copy
        filename = driver.find_element("css selector", ".list_c.ypiconitem dd").text
        self.assertEqual(filename, "copy")


    #移动文件夹
    def test_07_removefolder(self):
        if Test_Cloud.hasfolder == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        #新建一个ctest文件夹来完成这项功能
        driver.find_element("xpath", "//span[text()='新建文件夹']").click()
        sleep(1)
        # 输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("ctest")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        #把ctest1移动到ctest里面
        driver.find_element("xpath", "//dd[text() = 'ctest1']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='移动到']").click()
        sleep(2)
        #选中ctest前面的小框
        driver.find_element("xpath","//span[text()='ctest']//preceding-sibling::span[1]").click()
        #确定按钮
        driver.find_element('css selector',"#ypPopDirTreeWin .dialog-button a.l-btn .icon-ok").click()
        sleep(1)
        #捕捉移动成功的提示，如果没有提示会报错，提示元素未找到
        driver.find_element("xpath","//*[text()='移动成功']")
        sleep(3)
        #判断移动成功后当前目录下没有ctest1了
        result=self.isElementExist("//dd[text() = 'ctest1']")
        self.assertFalse(result)
        # 打开ctest，判断移动成功后ctest1在里面
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='打开']").click()
        sleep(2)
        #比对文件夹名称为ctest1
        filename = driver.find_element("css selector", ".list_c.ypiconitem dd").text
        self.assertEqual(filename, "ctest1")

    #文件夹属性
    def test_08_folderattr(self):
        driver = self.driver
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(3)
        driver.find_element("xpath", "//span[text()='属性']").click()
        sleep(2)
        #检查文件夹名字
        name=driver.find_element("xpath","//div[@title='ctest']").text
        self.assertIn('ctest',name)
        #检查创建者
        creator=driver.find_element("xpath","//*[@class=' file_xx']//li[5]//span[2]").text
        self.assertTrue(creator,'auto22@sic-ca.com')
        #检查作者
        owner = driver.find_element("xpath", "//*[@class=' file_xx']//li[6]//span[2]").text
        self.assertTrue(owner, 'auto22')

    #删除文件夹
    def test_09_delfolder(self):
        driver = self.driver
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='删除']").click()
        sleep(2)
        #删除确认按钮
        driver.find_element("css selector",".messager-window .icon-ok").click()
        sleep(10)
        # 判断删除成功后当前目录下没有ctest了
        result = self.isElementExist("//dd[text() = 'ctest']")
        self.assertFalse(result)

    # 打开文件
    def test_10_openfile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='打开']").click()
        sleep(2)
        #切换到新页面
        driver.switch_to.window(driver.window_handles[-1])
        #检查页面标题
        self.assertEqual(driver.title, "查看文件")
        #检查文件标题
        name=driver.find_element("css selector",".yp_r_doc_title .ypfile_title").text
        self.assertEqual(name, "test.png")
        #检查文件大小
        info=driver.find_element("css selector",".yp_r_info>li:nth-child(4)").text
        #self.assertEqual(info, "大小：80.7KB")
        driver.close()
        #返回原页面
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)
        #原页面有此文件，说明返回成功，因为新页面也有相应的文字，所以这边不用文字定位
        filename = driver.find_element("css selector", ".list_c.ypiconitem[isimage='1'] dd").text
        self.assertEqual(filename, "test.png")


    #网盘发邮件功能
    def test_11_fsendmail(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='发邮件']").click()
        sleep(2)
        #自动跳到发邮件窗口，核实附件名称
        name=driver.find_element("css selector","#file_upload_1-queue .fileName>div").text
        self.assertEqual(name, "test.png (80.7KB)")
        #填写邮件收件人
        driver.find_element("css selector","input.mailaddbox_input.ac_input").send_keys("auto22@sic-ca.com")
        #填写邮件主题为test
        driver.find_elements("css selector","[name='subject']")[3].send_keys("test")
        sleep(3)
        #点击发送按钮
        driver.find_elements("css selector",".modify_dom a[type='send']")[1].click()
        #10秒后进入收件箱
        sleep(10)
        driver.find_element("css selector","[cname='收件箱']").click()
        sleep(1)
        #查收主题为test的邮件
        driver.find_element("xpath", "//td[@field='subject']//b[text()='test']").click()
        sleep(1)
        #检查附件名为test.png
        filename=driver.find_element("css selector",'p.yulan').text
        self.assertEqual(filename, "test.png")

    #分享文件
    def test_12_sharefile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='分享']").click()
        sleep(2)
        # 进入分享弹框,中间输入名字，点击搜索
        driver.find_element("id", "serachid").send_keys("崔丽丽")
        # 中间小搜索框的搜索按钮
        driver.find_element("id", "sousuoid").click()
        sleep(1)
        #点击名字前面的单选框
        driver.find_element("css selector", ".tree-checkbox.tree-checkbox0").click()
        sleep(1)
        # 用js把滚动条拉到最下面
        js = "document.getElementById('ypBtnPopWin_share').scrollTop = 100000"
        driver.execute_script(js)
        driver.find_element("xpath", "//*[text()='立即分享']").click()
        sleep(3)
        # 进入我的分享页面
        driver.find_element("xpath", "//span[contains(text(),'我的分享')]").click()
        sleep(2)
        # 比对文件名一样说明分享成功
        name= driver.find_element("css selector",".iconUl dd").text
        self.assertEqual(name, "test.png")

        # 刷新页面，开始裢接分享
        driver.refresh()
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        # 进入裢接分享标签
        driver.find_element("css selector", ".share_links").click()
        # 点击分享裢接
        driver.find_element("xpath", "//*[@ctype='save']").click()
        # 点击复制裢接
        driver.find_element("xpath", "//*[@ctype='copy']").click()
        sleep(1)
        # 判断提示复制成功
        txt = driver.find_element("id", "infoPopDiv").text
        self.assertEqual(txt, "复制成功")

        # 刷新页面，开始邮件分享
        driver.refresh()
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        # 进入发到邮箱标签
        driver.find_element("css selector", ".send_mail").click()
        # 点击邮件分享按钮
        driver.find_element("xpath", "//*[@ctype='sendMail']").click()
        sleep(1)
        # 跳到发件页面，切换frame
        driver.switch_to.frame(driver.find_element("css selector", ".ke-edit-iframe"))
        # 判断发件内容有相关字样
        s = driver.find_element("css selector", ".ke-content").text
        self.assertEqual(s, "您的朋友和您分享了文件：test.png 请点击文件名查看")

    #下载文件
    def test_13_download(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        #先判断下本地下载路径下是否已经有此文件了
        path = "C:\\Users\\cll\\Downloads\\test.png"
        if os.path.exists(path):
            #如果有就删除
            os.remove(path)
        else:
            pass
        driver = self.driver
        #开始文件下载操作
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[@class][text()='下载']").click()
        sleep(8)
        #检测本地下载路径下有此文件，说明下载成功
        result=os.path.exists(path)
        self.assertTrue(result)

    #文件重命名
    def test_14_renamefile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='test.png']").click()
        sleep(2)
        driver.find_element("xpath", "//span[text()='重命名']").click()
        sleep(2)
        # 输入文件名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("test1")
        sleep(2)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        # 检查文件名字
        filename = driver.find_element("xpath","//dd[contains(text(),'.png')]").text
        self.assertEqual(filename, "test1.png")
        # #检查之前的名字不存在了
        # result=self.isElementExist("//*[text()='test.png']")
        # self.assertFalse(result)

    #移动文件
    def test_15_removefile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        # 新建一个ctest文件夹来完成这项功能
        driver.find_element("xpath", "//span[text()='新建文件夹']").click()
        sleep(1)
        # 输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("ctest")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        # 把test1.png移动到文件夹里面
        driver.find_element("xpath", "//dd[contains(text(),'.png')]").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='移动到']").click()
        sleep(2)
        # 选中ctest前面的小框
        driver.find_element("xpath", "//span[text()='ctest']//preceding-sibling::span[1]").click()
        # 确定按钮
        driver.find_element('css selector', "#ypPopDirTreeWin .dialog-button a.l-btn .icon-ok").click()
        sleep(1)
        # 捕捉移动成功的提示，如果没有提示会报错，提示元素未找到
        driver.find_element("xpath", "//*[text()='移动成功']")
        sleep(3)
        # 判断移动成功后当前目录下没有了
        out = self.isElementExist("//dd[contains(text(),'.png')]")
        self.assertFalse(out)
        # 打开ctest，判断移动成功后文件在里面
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='打开']").click()
        sleep(2)
        inner = self.isElementExist("//dd[contains(text(),'.png')]")
        self.assertTrue(inner)

    #复制文件
    def test_16_copyfile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='上传文件']").click()
        sleep(1)
        # 向上传框输入文件地址
        filepath = os.path.join(os.getcwd(), "file.png")
        driver.find_element("id", "select_btn_1").send_keys(filepath)
        sleep(4)
        #点击上传框的关闭按钮
        driver.find_element("css selector",".panel-tool-close").click()
        sleep(1)
        driver.find_element("xpath", "//*[text()='file.png']").click()
        sleep(3)
        driver.find_element("xpath", "//span[text()='复制到']").click()
        sleep(2)
        # 选中ctest前面的小框
        driver.find_element("xpath", "//span[text()='ctest']//preceding-sibling::span[1]").click()
        # 确定按钮
        driver.find_element('css selector', "#ypPopDirTreeWin .dialog-button a.l-btn .icon-ok").click()
        sleep(1)
        # 捕捉移动成功的提示，如果没有提示会报错，提示元素未找到
        driver.find_element("xpath", "//*[text()='复制成功']")
        sleep(3)
        # 判断复制成功后当前目录下还有
        out=self.isElementExist("//dd[text() = 'file.png']")
        self.assertTrue(out)
        # 打开ctest，判断复制成功后文件在里面
        driver.find_element("xpath", "//*[text()='ctest']").click()
        sleep(1)
        driver.find_element("xpath", "//span[text()='打开']").click()
        sleep(2)
        inner = self.isElementExist("//dd[text() = 'file.png']")
        self.assertTrue(inner)
        Test_Cloud.hasfile=True

    #属性功能
    def test_17_attribute(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='file.png']").click()
        sleep(3)
        driver.find_element("xpath", "//span[text()='属性']").click()
        sleep(2)
        #打开属性标签页，第一个tab页
        titlename=driver.find_elements("css selector","span.tabs-title")[0].text
        #核实标题是基本信息
        assert titlename=="基本信息"
        #第一个tab页上面文件名处
        filename=driver.find_element("css selector",".yp_fx>div div").get_attribute("title")
        #核实文件名显示正常
        self.assertEqual(filename,"file.png")
        # 检查创建者
        creator = driver.find_element("xpath", "//*[@class=' file_xx']//li[5]//span[2]").text
        self.assertTrue(creator, 'auto22')
        # 检查作者
        owner = driver.find_element("xpath", "//*[@class=' file_xx']//li[6]//span[2]").text
        self.assertTrue(owner, 'auto22')

    #删除文件
    def test_18_delfile(self):
        if Test_Cloud.hasfile == False:
            self.skipTest('直接跳过演示')
        driver = self.driver
        driver.find_element("xpath", "//*[text()='file.png']").click()
        sleep(3)
        driver.find_element("xpath", "//span//span[text()='删除']").click()
        sleep(2)
        #删除确认按钮
        driver.find_element("css selector", ".messager-window .icon-ok").click()
        sleep(5)
        # 判断移动成功后当前目录下没有file.png了
        result = self.isElementExist("//dd[text() = 'file.png']")
        self.assertFalse(result)

    #我的分享--查看裢接
    def test_19_checkshare(self):
        #新建一个cshare文件夹
        driver = self.driver
        driver.find_element("xpath", "//span[text()='新建文件夹']").click()
        sleep(1)
        # 输入文件夹名称
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys("cshare")
        sleep(1)
        # 输入回车
        driver.find_element("css selector", ".list_c.ypiconitem dd input").send_keys(Keys.ENTER)
        sleep(3)
        #分享一下
        driver.find_element("xpath", "//*[text()='cshare']").click()
        sleep(2)
        driver.find_element("xpath", "//span[text()='分享']").click()
        sleep(2)
        # 进入分享弹框,中间输入名字，点击搜索
        driver.find_element("id", "serachid").send_keys("崔丽丽")
        driver.find_element("id", "sousuoid").click()
        sleep(1)
        # 中间小搜索框的搜索按钮
        driver.find_element("css selector", ".tree-checkbox.tree-checkbox0").click()
        sleep(1)
        # 用js把滚动条拉到最下面
        js = "document.getElementById('ypBtnPopWin_share').scrollTop = 100000"
        driver.execute_script(js)
        driver.find_element("xpath", "//*[text()='立即分享']").click()
        sleep(3)
        #进入我的分享页面
        driver.find_element("xpath", "//span[contains(text(),'我的分享')]").click()
        sleep(2)
        driver.find_element("xpath", "//*[text()='cshare']").click()
        sleep(2)
        driver.find_element("xpath", "//*[text()='查看链接']").click()
        sleep(2)
        #检查查看链接弹出窗口的标题
        name=driver.find_element("css selector",".yp_fx div div").get_attribute("title")
        assert name == "cshare"
        #检查查看链接弹出窗口的所有者
        author=driver.find_elements("css selector",".wjsx_tit+span")[4].text
        self.assertEqual(author,"auto22")
        #点击关闭按钮
        sleep(2)
        driver.find_element("xpath", "//span//span[text()='关闭']").click()


    #我的分享--访问日志
    def test_20_sharelog(self):
        driver=self.driver
        # 进入我的分享页面
        driver.find_element("xpath", "//span[contains(text(),'我的分享')]").click()
        sleep(3)
        driver.find_element("xpath", "//*[text()='cshare']").click()
        sleep(2)
        #先制造个访问日志，不然进去是空的，双击访问一下文件夹制造访问记录
        actions = ActionChains(driver=driver)
        actions.double_click(driver.find_element("xpath", "//*[text()='cshare']")).perform()
        sleep(2)
        driver.find_element("xpath", "//*[text()='上一级']").click()
        sleep(2)
        #点击进入访问日志
        driver.find_element("xpath", "//*[text()='cshare']").click()
        sleep(2)
        driver.find_element("xpath", "//span[contains(text(),'访问日志')]").click()
        #查看弹出窗口的浏览记录
        sleep(2)
        name=driver.find_element("css selector",".click_sele>td:nth-child(1)").text
        #核实访问者用户名为auto22
        self.assertEqual(name,"auto22")
        driver.find_element("css selector",".panel-tool-close").click()

    #我的分享--取消分享功能
    def test_21_sharecancel(self):
        driver = self.driver
        # 进入我的分享页面
        driver.find_element("xpath", "//span[contains(text(),'我的分享')]").click()
        sleep(2)
        driver.find_element("xpath", "//*[text()='cshare']").click()
        sleep(3)
        driver.find_element("xpath", "//span[text()='取消分享']").click()
        #取消分享后弹出的确认窗口，点击确定
        driver.find_element("css selector",".messager-button .icon-ok").click()
        #验证操作成功的提示
        result=driver.find_element("id","infoPopDiv").text
        self.assertEqual(result, "操作成功")
        sleep(3)
        #验证分享的文件夹不存在
        result1=self.isElementExist("//*[text()='cshare']")
        self.assertFalse(result1)


if __name__ == '__main__':
    unittest.main(verbosity=2)