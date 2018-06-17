#!usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'NiHua'
# hua.ni@socialcredits.cn


import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
import uuid

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor, RealDictCursor
from contextlib import contextmanager

from scpy.logger import get_logger

logging = get_logger(__file__)
sys.path.append("..")

# pg 数据库配置
PG_HOST = '192.168.31.157'
PG_DATABASE = 'decision_engine_dev'
PG_USER = 'decision_engine_dev'
PG_PASSWORD = '1qaz2wsx'
PG_PORT = '5432'


class PgScriptUtil():

    # __metaclass__ = Singleton
    def __init__(self, database=PG_DATABASE, user=PG_USER, password=PG_PASSWORD,
                 host=PG_HOST, port=PG_PORT):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.logger = get_logger(__file__)
        self.conn_pool = ThreadedConnectionPool(
            minconn=2,
            maxconn=20,
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def get_conn(self):
        conn = self.conn_pool.getconn()
        if not conn.autocommit:  # 检查并关闭事物处理
            conn.autocommit = True
        return conn

    @contextmanager
    def get_cursor(self, server_side=False):
        conn = self.conn_pool.getconn()
        try:
            if server_side:
                yield conn.cursor(uuid.uuid4().hex, cursor_factory=RealDictCursor)
                conn.commit()
            else:
                yield conn.cursor()
                conn.commit()
        finally:
            self.put_conn(conn)

    def put_conn(self, conn):
        self.conn_pool.putconn(conn)

    def query_all_sql(self, sql):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(sql)
            result_list = []
            for row in cur.fetchall():
                result_list.append(row)
            conn.commit()
        finally:
            self.put_conn(conn)
        return result_list

    def get_all_value(self, sql, param=()):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, param)
            result_list = []
            for row in cur.fetchall():
                result_list.append(row)
            conn.commit()
        finally:
            self.put_conn(conn)
        return result_list

    def query_one_sql(self, sql):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            conn.commit()
        finally:
            self.put_conn(conn)
        return dict(row) if row else {}

    def execute_sql(self, sql):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(sql)
            cur.close()
            conn.commit()
        finally:
            self.put_conn(conn)

    def execute_sql_no_result(self, sql_and_params):
        """
        执行不返回
        :type sql_and_params tuple
        :param sql_and_params:
        :return:
        """
        sql = sql_and_params[0]
        params = sql_and_params[1]
        conn = self.get_conn()
        cur = conn.cursor(cursor_factory=DictCursor)
        try:
            cur.execute(sql, params)
        except Exception, e:
            self.__logging_error_message(sql, params)
            raise e
        finally:
            self.__close_conn(cur, conn)

    def execute_insert_sql(self, sql, values):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(sql, values)
            cur.close()
            conn.commit()
        finally:
            self.put_conn(conn)

    def execute_insert_sql_with_return_id(self, sql, values):
        '''
        插入并返回此记录的Id
        sql_string = "INSERT INTO domes_hundred (name,name_slug,status) VALUES (%s,%s,%s) RETURNING id;"
        Just to clarify, the id in RETURNING id should be the field name of the serial / primary key field
        :param sql:
        :param values:
        :return:
        '''
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(sql, values)
            id = cur.fetchone()[0]
            cur.close()
            conn.commit()
        finally:
            self.put_conn(conn)
        return id

    def execute_non_query(self, sql, param=()):
        """执行sql语句<增，删，改>，没有返回值"""
        with self.get_cursor() as cursor:
            try:
                sql = self.log(sql, cursor, param)
                cursor.execute(sql)
            except Exception, e:
                traceback.print_exc(e)
                self.logger.error(e)

    def is_exists_data(self, sql, param=()):
        """判断数据是否存在"""
        is_exist = False
        with self.get_cursor() as cursor:
            try:
                sql = self.log(sql, cursor, param)
                cursor.execute(sql)
                data = cursor.fetchone()
                if data:
                    is_exist = True
            except Exception, e:
                self.logger.error(e)

        return is_exist

    def get_many(self, sql, param=()):
        """获取多条数据"""
        with self.get_cursor(server_side=True) as cursor:
            try:
                sql = self.log(sql, cursor, param)
                cursor.itersize = 10
                cursor.execute(sql)
                result_list = []
                for row in cursor.fetchall():
                    result_list.append(row)

            except Exception, e:
                self.logger.error(e)

    def get_single_value(self, sql, param=()):
        """获取首行首列的值"""
        with self.get_cursor() as cursor:
            try:
                sql = self.log(sql, cursor, param)
                cursor.execute(sql)
                return cursor.fetchone()[0]
            except Exception, e:
                self.logger.error(e)
                return None

    def get_one_value(self, sql, param=()):
        conn = self.get_conn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(sql, param)
            row = cur.fetchone()
            cur.close()
            conn.commit()
        finally:
            self.put_conn(conn)
        return dict(row) if row else {}

    def log(self, sql, cursor, param=()):
        try:
            sql = cursor.mogrify(sql, param)
        except Exception, e:
            self.logger.error(e)
        import re
        self.logger.info(re.subn(r'[ ]{0,}\n[ ]{0,}', '', sql)[0])
        return sql

    def updata_one(self, sql, param=()):
        """判断数据是否存在"""
        is_exist = False
        with self.get_cursor() as cursor:
            try:
                sql = self.log(sql, cursor, param)
                cursor.execute(sql)
                is_exist = True
            except Exception, e:
                self.logger.error(e)
                is_exist = False

        return is_exist

    def __close_conn(self, cur, conn):
        """
        推回连接池 -- 无事物处理情况
        """
        cur.close()
        self.put_conn(conn)

    @staticmethod
    def __logging_error_message(sql, params):
        error_str = 'Inner exception: execute sql:' + sql + '; params:' + str(params)
        logging.error(error_str)
        return error_str


def get_company_names01(path):
    company_names = []
    with open(path) as f:
        for data in f.readlines():
            if data.startswith('#'):
                continue
            name = data.decode('utf-8')
            # print name
            company_names.append(name.strip("\n"))
    return company_names



def is_none(d):
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')
if __name__ == '__main__':
    '''
    '''
    import json

    pg = PgScriptUtil()
    not_bankrupt_list = []
    sql_request = '''SELECT   company_name  FROM all_features WHERE company_name = %s'''
    bankrupt_company = get_company_names01(
        "/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company.txt")
    bankrupt_company = list(set(bankrupt_company))
    for company in bankrupt_company:
            company = company.strip("").strip("\n")
            # company ='%'+company+'%'
            param = ((company,))
            res = pg.get_all_value(sql_request, param)
            if res.__len__() <= 0:
                po1 = company.find("债务人")
                po2 = company.find("公司")
                if po1 < 0 or po2 < 0:
                    po1 = company.find("申请人")
                    po2 = company.find("公司")
                    if po1 < 0 or po2 < 0: continue
                    company_name = company[po1 + 3:po2 + 2].replace('\t', '').replace('\n', '').replace(' ', '')
                else:
                    company_name = company[po1 + 3:po2 + 2].replace('\t', '').replace('\n', '').replace(' ', '')
                    if is_none(company_name): continue
                param = ((company,))
                res = pg.get_all_value(sql_request, param)
                if res.__len__() <= 0:
                    continue
            else:
                not_bankrupt_list.append(company)

    f1 = open('/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company_ok.txt', 'w')

    for company in not_bankrupt_list:
        company = company + "\n"
        f1.write(company)

    f1.flush()
    f1.close()

    print(not_bankrupt_list.__len__())

    print(json.dumps(not_bankrupt_list, ensure_ascii=False, indent=4, default=lambda x: str(x)))
