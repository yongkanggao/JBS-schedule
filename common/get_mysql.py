#coding=utf-8
#author_="bruce.gao"
#date:2019/10/8 17:02

import pymysql
from common.read_config import ReadConfig
from common.config_log import Log

class GetMySql(object):
    def __init__(self):
        self.config = ReadConfig()
        self.log = Log()
        self.host = self.config.get_mysql('host')
        self.port = int(self.config.get_mysql('port'))
        self.user = self.config.get_mysql('user')
        self.password = self.config.get_mysql('passwd')
        self.database = self.config.get_mysql('database')

    def connect(self):
        try:
            self.db = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8'
            )
            self.log.info('连接数据库成功')
        except Exception as error:
            self.log.error('连接数据库失败！！！！')
            self.log.error(error)
        else:
            self.cursor = self.db.cursor()
            self.log.info('成功创建数据库游标')

    def close(self):
        try:
            self.db.close()
            self.cursor.close()
            self.log.info('数据库连接关闭')
        except Exception as error:
            self.log.error('数据库连接关闭失败！！！！')
            self.log.error(error)

    def select(self, sql):
        my_result = ''
        try:
            self.cursor.execute(sql)
            my_result = self.cursor.fetchall()
        except Exception as error:
            self.log.error('查询失败')
            self.log.error(error)
        return my_result

if __name__ =='__main__':
    sql = ReadConfig().get_trade("today_to_7day")
    db = GetMySql()
    db.connect()
    result = db.select(sql)
    db.close()
    print(result)