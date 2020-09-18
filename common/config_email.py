import os
import win32com.client as win32
import datetime
from common import get_path_info, read_config
from common.config_log import Log

class SendEmail(object):

    def __init__(self):
        read_conf = read_config.ReadConfig()
        self.subject = read_conf.get_email('subject')  # 从配置文件中读取，邮件主题
        self.app = str(read_conf.get_email('app'))  # 从配置文件中读取，邮件类型
        self.addressee = read_conf.get_email('addressee')  # 从配置文件中读取，邮件收件人
        self.cc = read_conf.get_email('cc')  # 从配置文件中读取，邮件抄送人
        self.mail_path = os.path.join(get_path_info.get_path(), 'report', 'report.html')  # 获取测试报告路径
        self.logger = Log()

    def outlook(self):
        olook = win32.Dispatch("%s.Application" % self.app)
        mail = olook.CreateItem(0)
        mail.To = self.addressee # 收件人
        mail.CC = self.cc # 抄送
        mail.Subject = str(datetime.datetime.now())[0:19]+'%s' %self.subject#邮件主题
        mail.Attachments.Add(self.mail_path, 1, 1, "myFile")
        content = """
                    执行测试中……
                    测试已完成！！
                    生成报告中……
                    报告已生成……
                    报告已邮件发送！！
                    """
        mail.Body = content
        mail.Send()
        print('send email ok!!!!')
        self.logger.info('send email ok!!!!')

if __name__ == '__main__':# 运营此文件来验证写的send_email是否正确
    print(subject)
    SendEmail().outlook()
    print("send email ok!!!!!!!!!!")