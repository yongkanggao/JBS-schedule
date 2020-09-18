import os
import common.HTMLTestRunner as HTMLTestRunner
import unittest
from common import get_path_info
from common.read_config import ReadConfig
from common.config_email import SendEmail
from common.config_log import Log

send_mail = SendEmail()
path = get_path_info.get_path()
report_path = os.path.join(path, 'report')
on_off = ReadConfig().get_email('on_off')
log = Log()

class AllTest(object):#定义一个类AllTest
    def __init__(self):#初始化一些参数和数据
        global resultPath
        resultPath = os.path.join(report_path, "report.html")#report.html
        self.caseFile = os.path.join(path, "schedule")#真正的测试断言文件路径
        log.info('resultPath'+resultPath)#将resultPath的值输入到日志，方便定位查看问题

    def set_case_suite(self):
        """
        循环遍历
        :return:
        """
        test_suite = unittest.TestSuite()
        suite_module = []
        discover = unittest.defaultTestLoader.discover(self.caseFile, pattern='schedule.py', top_level_dir=None)
        suite_module.append(discover)#将discover存入suite_module元素组
        print('suite_module:'+str(suite_module))
        if len(suite_module) > 0:#判断suite_module元素组是否存在元素
            for suite in suite_module:#如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:#从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite#返回测试集

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()#调用set_case_suite获取test_suite
            print('try')
            print(str(suit))
            if suit is not None:#判断test_suite是否为空
                print('if-suit')
                fp = open(resultPath, 'wb')#打开report.html测试报告文件，如果不存在就创建
                #调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                print("Have no case to test.")
        except Exception as ex:
            print(str(ex))
            log.error(str(ex))

        finally:
            print("*********TEST END*********")
            fp.close()
        #判断邮件发送的开关
        if on_off == 'on':
            send_mail.outlook()
        else:
            print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")

if __name__ == '__main__':
    AllTest().run()


