# -*- coding: utf-8 -*-
# @Time : 2020/9/24 16:34
# @Author : Bruce.Gao
# @FileName: get_es.py
# @Software: PyCharm

from elasticsearch5 import Elasticsearch
from common.read_config import ReadConfig
from common.config_log import Log
config = ReadConfig()
log = Log()
import time
import demjson

now_time = int(time.time())
zero_time = now_time - now_time % 86400 + time.timezone
last_time = zero_time + 86399

class GetElasticSearch(object):

    def __init__(self):
        self.host = config.get_elasticsearch('host')
        self.port = config.get_elasticsearch('port')
        self.user = config.get_elasticsearch('user')
        self.passwd = config.get_elasticsearch('passwd')

    def conn_es(self):
        # 创建elasticsearch客户端
        self.es = Elasticsearch(
            # elasticsearch集群服务器的地址
            [{'host': self.host,'port': self.port}],
            # 启动前嗅探es集群服务器
            sniff_on_start=True,
            # es集群服务器结点连接异常时是否刷新es节点信息
            sniff_on_connection_fail=True,
            # 每60秒刷新节点信息
            sniffer_timeout=60
        )

    def query(self, index, body, doc_type='_doc'):
        self.conn_es()
        ret = self.es.search(index=index, body=body, doc_type=doc_type)
        return ret

if __name__ == '__main__':
    es = GetElasticSearch()
    body = {
    "query":{
        "range":{
            "tradeTime":{
            "gte":int(round(zero_time * 1000)),
            "lte":int(round(last_time * 1000))
}
        }
    }
}
    response = es.query('trade_order_index', body)
    print(response['hits']['hits'][0]['_source'])
