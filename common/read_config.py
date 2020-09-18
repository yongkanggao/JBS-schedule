import os
import configparser
from common import get_path_info

class ReadConfig(object):

    def __init__(self):
        path = get_path_info.get_path()  # 调用实例化，
        config_path = os.path.join(path, 'config/config.ini')  # 这句话是在path路径下再加一级
        self.config = configparser.ConfigParser()  # 调用外部的读取配置文件的方法
        self.config.read(config_path, encoding='utf-8')

    def get_email(self, name):
        value = self.config.get('EMAIL', name)
        return value

    def get_mysql(self, name):
        value = self.config.get('DATABASE', name)
        return value

    def get_trade(self,name):
        value = self.config.get('Trade_Order',name)
        return value

    def get_delivery(self,name):
        value = self.config.get('Delivery_Order',name)
        return value

if __name__ == '__main__':#测试一下，我们读取配置文件的方法是否可用
    print('Trade_Order的sql：', ReadConfig().get_trade('today'))



