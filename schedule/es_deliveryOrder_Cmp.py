# -*- coding: utf-8 -*-
# @Time : 2020/9/29 13:38
# @Author : Bruce.Gao
# @FileName: es_deliveryOrder_Cmp.py
# @Software: PyCharm

from common.get_es import GetElasticSearch
import unittest
import paramunittest
from common.read_excel import ReadExcel
from common.config_log import Log
from common import get_mysql
import json
import time
import warnings
global true,false
true = True
false = False

last_hour_time = int(round(int(time.time()))) * 1000 - 3600000  #当前时间前一小时以毫秒显示的时间戳
last_Twohour_time = last_hour_time - 3600000   #当前时间前两小时的时间戳

logger = Log()
DeliveryOder_Es_Cmp_xls = ReadExcel().get_xls('order.xlsx', 'DeliveryOder_Es_Cmp')

@paramunittest.parametrized(*DeliveryOder_Es_Cmp_xls)
class TestDeliveryOder_Es_Cmp_xls(unittest.TestCase):
    """
    销售出库单同步到ES
    """
    def setParameters(self,case_name,sql,es_search):
        """
        set params
        :param case_name:
        :param sql
        :param es_search
        :return:
        """
        self.case_name = str(case_name)
        self.sql = str(sql)
        self.es_search = str(es_search)

    def setUp(self):
        """
        :return:
        """
        warnings.simplefilter('ignore', ResourceWarning)
        print("\n" + self.case_name + ":\n\n比对开始：\n")

    def tearDown(self):
        print("\n\n比对结束\n\n")

    def test_checkResult(self):
        db = get_mysql.GetMySql()
        db.connect()
        result = db.select(self.sql)
        if result != ():
            jsdata = []
            #将查询出的mysql数据组装成字典数据
            for i in range(len(result)):
                response = {}
                response['deliveryOrderId'] = str(result[i][0])
                response['orderId'] = str(result[i][1])
                response['sourceOrderId'] = str(result[i][2])
                response['platCode'] = str(result[i][3])
                response['orderType'] = int(result[i][4])
                response['outDeliveryOrderId'] = str(result[i][5])
                response['warehouseCode'] = str(result[i][6])
                response['warehouseOutCode'] = str(result[i][7])
                response['warehouseType'] = int(result[i][8])
                if result[i][9] != None:
                    response['tradeTime'] = int(time.mktime(time.strptime(str(result[i][9]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][10] != None:
                    response['payTime'] = int(time.mktime(time.strptime(str(result[i][10]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['codAmount'] = str(result[i][11])
                response['deliveryCondition'] = int(result[i][12])
                response['ownerCode'] = str(result[i][13])
                response['shopName'] = str(result[i][14])
                response['shopCode'] = str(result[i][15])
                response['cartonCode'] = str(result[i][16])
                response['expressCode'] = str(result[i][17])
                response['buyerName'] = str(result[i][18])
                if result[i][19] != None:
                    response['sendTime'] = int(time.mktime(time.strptime(str(result[i][19]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][20] != None:
                    response['warehouseDeliveryTime'] = int(time.mktime(time.strptime(str(result[i][20]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['logisticsCode'] = str(result[i][21])
                response['platLogisticsCode'] = str(result[i][22])
                response['logisticsOutCode'] = str(result[i][23])
                response['senderName'] = str(result[i][24])
                response['senderMobile'] = str(result[i][25])
                response['senderProvince'] = str(result[i][26])
                response['senderCity'] = str(result[i][27])
                response['senderDistrict'] = str(result[i][28])
                response['senderDetailAddress'] = str(result[i][29])
                response['receiverName'] = str(result[i][30])
                response['receiverMobile'] = str(result[i][31])
                response['receiverProvince'] = str(result[i][32])
                response['receiverCity'] = str(result[i][33])
                response['receiverDistrict'] = str(result[i][34])
                response['receiverDetailAddress'] = str(result[i][35])
                response['orderStatus'] = int(result[i][36])
                response['sourcePlatformCode'] = str(result[i][37])
                response['undoId'] = str(result[i][38])
                response['printed'] = int(result[i][39])
                response['zipCode'] = str(result[i][40])
                response['templateUrl'] = str(result[i][41])
                response['customTemplateUrl'] = str(result[i][42])
                if result[i][43] != None:
                    response['nextPushTime'] = int(time.mktime(time.strptime(str(result[i][43]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['pushFailMsg'] = str(result[i][46])
                response['buyerRemark'] = str(result[i][47])
                response['sellerRemark'] = str(result[i][48])
                if result[i][49] != None:
                    response['logisticsType'] = int(result[i][49])
                response['printNum'] = int(result[i][50])
                jsdata.append(response)
                # print(jsdata)
            ress = []
            for k in range(len(jsdata)):
                for j in list(jsdata[k].keys()):
                    if jsdata[k][j] == '':
                        del jsdata[k][j]
                ress.append(jsdata[k])
                data = eval(json.dumps(ress, ensure_ascii=False, indent=1))

            #ES查询数据
            es = GetElasticSearch()
            response = es.query('delivery_order_fat_index', eval(self.es_search))
            res_data = response['hits']['hits']
            time.sleep(3)

            mysql_data = []
            for m in range(len(data)):
                mysql_data.append(data[m]['sourceOrderId'])
            # print(mysql_data)
            es_data = []
            for n in range(len(res_data)):
                es_data.append(res_data[n]['_source']['sourceOrderId'])
            # print(es_data)

            data_set = set(mysql_data) ^ set(es_data)  #比较原始订单号是否一致
            # print(data_set)
            if data_set != set():
                print("订单有遗漏到ES\n")
                for i in range(len(data_set)):
                    print("原始订单为：" + tuple(data_set)[i] + "\n")
            for u in range(len(data)):
               for v in range(len(res_data)):
                   if data[u]['sourceOrderId'] == res_data[v]['_source']['sourceOrderId']:
                       dict1 = data[u]
                       dict2 = res_data[v]['_source']
                       dict2['codAmount'] = format(dict2['codAmount'], '.4f')
                       diff = dict1.keys() & dict2
                       diff_vals = [(p, dict1[p], dict2[p]) for p in diff if dict1[p] != dict2[p]]   #原始订单号一致时，比较内容是否一致
                       # print(diff_vals)
                       if diff_vals != []:
                           print("ES数据同步不正确，原始订单为：" + dict1['sourceOrderId'])
                           print("数据不一致为:" + str(diff_vals))
                       # else:
                       #     print("数据同步一致")
                       self.assertEqual(diff_vals, [])
        else:
            print("没有新的订单\n")

if __name__ == '__main__':
    unittest.main()