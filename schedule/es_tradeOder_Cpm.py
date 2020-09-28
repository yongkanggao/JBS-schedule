# -*- coding: utf-8 -*-
# @Time : 2020/9/27 10:09
# @Author : Bruce.Gao
# @FileName: es_tradeOder_Cpm.py
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
TradeOder_Es_Cmp_xls = ReadExcel().get_xls('order.xlsx', 'TradeOder_Es_Cmp')

@paramunittest.parametrized(*TradeOder_Es_Cmp_xls)
class TestTradeOder_Es_Cmp_xls(unittest.TestCase):
    """
    系统订单同步到ES
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
                response['orderId'] = str(result[i][0])
                response['sourceOrderId'] = str(result[i][1])
                response['deliveryOrderId'] = str(result[i][2])
                response['platCode'] = str(result[i][3])
                response['shopId'] = str(result[i][4])
                response['shopCode'] = str(result[i][5])
                response['shopName'] = str(result[i][6])
                response['tradeStatus'] = int(result[i][7])
                response['innerStatus'] = int(result[i][8])
                if result[i][9] != 0:
                    response['stepTradeTtatus'] = int(result[i][9])
                response['stepPidFee'] = float(result[i][10])
                response['tradeTime'] = int(time.mktime(time.strptime(str(result[i][11]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][12] != None:
                    response['payTime'] = int(time.mktime(time.strptime(str(result[i][12]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][13] != None:
                    response['completeTime'] = int(
                        time.mktime(time.strptime(str(result[i][13]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['buyerRemark'] = str(result[i][14])
                response['sellerRemark'] = str(result[i][15])
                response['auditRemark'] = str(result[i][16])
                response['isMultiMerge'] = bool(ord(result[i][17]))
                response['remarkFlag'] = str(result[i][18])
                response['orderCategory'] = int(result[i][19])
                response['markId'] = str(result[i][20])
                response['buyerName'] = str(result[i][21])
                response['payId'] = str(result[i][22])
                response['payType'] = int(result[i][23])
                response['payAccount'] = str(result[i][24])
                response['receiverName'] = str(result[i][25])
                response['receiverCountry'] = str(result[i][26])
                response['receiverProvince'] = str(result[i][27])
                response['receiverCity'] = str(result[i][28])
                response['receiverDistrict'] = str(result[i][29])
                response['receiverprovinceCode'] = str(result[i][30])
                response['receiverCityCode'] = str(result[i][31])
                response['receiverDistrictCode'] = str(result[i][32])
                response['receiverAddress'] = str(result[i][33])
                response['receiverMobile'] = str(result[i][34])
                response['receiverTelno'] = str(result[i][35])
                response['receiverZip'] = str(result[i][36])
                response['totalFee'] = str(result[i][37])
                response['postFee'] = str(result[i][38])
                response['payment'] = str(result[i][39])
                response['discountFee'] = str(result[i][40])
                response['codAmount'] = str(result[i][41])
                response['dapAmount'] = str(result[i][42])
                response['invoiceType'] = int(result[i][43])
                response['invoiceTitle'] = str(result[i][44])
                response['invoiceContent'] = str(result[i][45])
                response['tradeFrom'] = int(result[i][46])
                response['orderType'] = int(result[i][47])
                response['goodsSpecies'] = int(result[i][48])
                response['goodsNum'] = int(result[i][49])
                response['refundStatus'] = int(result[i][50])
                response['splitStatus'] = bool(ord(result[i][51]))
                response['printRemark'] = str(result[i][52])
                if result[i][53] != None:
                    response['auditTime'] = int(time.mktime(time.strptime(str(result[i][53]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['auditBy'] = str(result[i][54])
                response['warehouseCode'] = str(result[i][55])
                response['warehouseOutCode'] = str(result[i][56])
                response['logisticsCode'] = str(result[i][57])
                response['ownerCode'] = str(result[i][58])
                response['expressCode'] = str(result[i][59])
                response['deliveryCondition'] = int(result[i][60])
                response['containGift'] = bool(ord(result[i][61]))
                response['checkOutStatus'] = bool(ord(result[i][62]))
                response['checkBy'] = str(result[i][63])
                response['frozenStatus'] = bool(ord(result[i][64]))
                response['frozenReasonId'] = str(result[i][65])
                response['interceptReason'] = str(result[i][66])
                response['failReason'] = str(result[i][67])
                response['cartonCode'] = str(result[i][68])
                response['innerMark'] = str(result[i][69])
                if result[i][70] != None:
                    response['nextSplitTime'] = int(
                        time.mktime(time.strptime(str(result[i][70]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][71] != None:
                    response['delayTime'] = int(time.mktime(time.strptime(str(result[i][71]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][72] != None:
                    response['splitTime'] = int(time.mktime(time.strptime(str(result[i][72]), "%Y-%m-%d %H:%M:%S"))) * 1000
                response['logisticsHasBack'] = bool(ord(result[i][73]))
                if result[i][74] != None:
                    response['commitTime'] = int(time.mktime(time.strptime(str(result[i][74]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][75] != None:
                    response['createTime'] = int(time.mktime(time.strptime(str(result[i][75]), "%Y-%m-%d %H:%M:%S"))) * 1000
                if result[i][76] != None:
                    response['updateTime'] = int(time.mktime(time.strptime(str(result[i][76]), "%Y-%m-%d %H:%M:%S"))) * 1000
                jsdata.append(response)
            ress = []
            for k in range(len(jsdata)):
                for j in list(jsdata[k].keys()):
                    if jsdata[k][j] == ''or jsdata[k] == 'createTime' or jsdata[k] == 'updateTime':
                        del jsdata[k][j]
                ress.append(jsdata[k])
                data = eval(json.dumps(ress, ensure_ascii=False, indent=1))

            #ES查询数据
            es = GetElasticSearch()
            response = es.query('trade_order_index', eval(self.es_search))
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
                       dict2['totalFee'] = format(dict2['totalFee'], '.4f')
                       dict2['postFee'] = format(dict2['postFee'], '.4f')
                       dict2['payment'] = format(dict2['payment'], '.4f')
                       dict2['discountFee'] = format(dict2['discountFee'], '.4f')
                       dict2['codAmount'] = format(dict2['codAmount'], '.4f')
                       dict2['dapAmount'] = format(dict2['dapAmount'], '.4f')
                       del dict2['createTime']
                       del dict2['updateTime']
                       diff = dict1.keys() & dict2
                       diff_vals = [(p, dict1[p], dict2[p]) for p in diff if dict1[p] != dict2[p]]   #原始订单号一致时，比较内容是否一致
                       if diff_vals != []:
                           print("ES数据同步不正确，原始订单为：" + dict1['sourceOrderId'])
                           print("数据不一致为:" + str(diff_vals))
        else:
            print("没有新的订单\n")

if __name__ == '__main__':
    unittest.main()