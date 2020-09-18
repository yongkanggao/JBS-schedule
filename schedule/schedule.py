# -*- coding: utf-8 -*-
# @Time : 2020/9/18 13:48
# @Author : Bruce.Gao
# @FileName: schedule.py
# @Software: PyCharm

import unittest
import paramunittest
from common.read_excel import ReadExcel
from common.config_log import Log
from common import get_mysql

logger = Log()
Order_xls = ReadExcel().get_xls('order.xlsx', 'Order')

@paramunittest.parametrized(*Order_xls)
class TestDelData_xls(unittest.TestCase):
    """
    删除数据
    """
    def setParameters(self,case_name,sql):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :return:
        """
        self.case_name = str(case_name)
        self.sql = str(sql)

    def setUp(self):
        """
        :return:
        """
        print("\n" + self.case_name + ":\n\n测试开始前准备\n")

    def tearDown(self):
        print("测试结束\n输出log\n完结!\n\n")

    def test_checkResult(self):
        db = get_mysql.GetMySql()
        db.connect()
        db.select(self.sql)
        print()
        print(db.select(self.sql))
        logger.info(str(self.case_name))

if __name__ == '__main__':
    unittest.main()