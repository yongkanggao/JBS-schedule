# -*- coding: utf-8 -*-
# 打印日志信息
"""
  ERROR：发生错误时，如IO操作失败或者连接问题
  WARNING：发生很重要的事件，但是并不是错误时，如用户登录密码错误
  INFO：处理请求或者状态变化等日常事务
  DEBUG：调试过程中使用DEBUG等级，如算法中每个循环的中间状态
"""
import logging
import time
import os
from common import get_path_info


class Log(object):
    def __init__(self):
        # 文件命名
        path = get_path_info
        self.log_path = os.path.join(path.get_path(), 'log')
        self.log_name = os.path.join(self.log_path, '%s.log' % time.strftime('%y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        # 区分日志级别
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == '__main__':
    log = Log()
    log.info("----------自动化测试开始----------")
    log.info("登录成功...")
    log.info('输入手势密码...')
    log.warning("-----------自动化测试结束----------")
