import unittest
import time
import os
from HTMLTestRunner import HTMLTestRunner

mt_dir=os.path.join(os.getcwd())

tests=unittest.defaultTestLoader.discover(mt_dir,pattern='mt_*.py')

now=time.strftime('%Y-%m-%d %H-%m-%S')

filename=mt_dir+'\\report\\'+now + '_result.html'

fp=open(filename,'wb')

runner=HTMLTestRunner(stream=fp,title='测试报告',description='webmail测试情况',verbosity=2)

runner.run(tests)