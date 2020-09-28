# -*- coding: utf-8 -*-
# @Time : 2020/9/18 13:48
# @Author : Bruce.Gao
# @FileName: tradeOrder_Cmp.py
# @Software: PyCharm

import unittest
import paramunittest
from common.read_excel import ReadExcel
from common.config_log import Log
from common import get_mysql

logger = Log()
Order_xls = ReadExcel().get_xls('order.xlsx', 'Order')

@paramunittest.parametrized(*Order_xls)
class TestOrderCmp_xls(unittest.TestCase):
    """
    订单转换比对
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
        print("\n" + self.case_name + ":\n\n比对开始：\n")

    def tearDown(self):
        print("\n\n比对结束\n\n")

    def test_checkResult(self):
        db = get_mysql.GetMySql()
        db.connect()
        result = db.select(self.sql)
        # logger.info(str(self.case_name))
        # self.assertEqual(result,())
        # print(result)
        if self.case_name.endswith("同步到系统订单数据"):
            data = set(str(result[1])[2:-3].split(',')) - set(str(result[0])[2:-3].split(','))
            if data == set():
                print("比对结果：系统订单数据没有遗漏")
            else:
                print("比对结果：系统订单数据有遗漏\n\n")
                for k in range(len(data)):
                    print("原始订单为：" + tuple(data)[k] + "\n")
        else:
            if result == ():
                print("比对结果：没有生成重复的数据")
            else:
                print("比对结果：有重复数据生成\n\n")
                for k in range(len(result)):
                    print("原始订单为："+ result[k][0])
                    print("对应系统订单为:" + result[k][1] + "\n")

if __name__ == '__main__':
    unittest.main()