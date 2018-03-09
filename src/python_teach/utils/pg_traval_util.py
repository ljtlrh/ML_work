#!usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'NiHua'
# hua.ni@socialcredits.cn


import sys
import traceback
import uuid
from scpy.logger import get_logger
sys.path.append("..")
from db_config import PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor, RealDictCursor
from contextlib import contextmanager

class PgUtil():
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
            cur.execute(sql,param)
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
                for row in cursor:
                    yield row
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


if __name__ == '__main__':
    # sql_request = '''select dimension, id from dimension where category='法务' or category='失信' or category='执行' '''
    sql_request = '''  select * from  client   u left join public."archive" arv on u.archive_id=arv.id
          where u.id=%s'''
    sql_request = sql_request % (442)
    pg = PgUtil()
    map_id = {}
    sql_request = """
        UPDATE   client
       SET  "type"= %s
         WHERE id = %s
       """
    param = (('A', 442))

    # for index in range(100):
    #     for row in pg.query_all_sql(sql_request):
    #         print row
    #         data_row = {row['dimension']: row['id']}
    #         map_id.update(data_row)
    #     time.sleep(1)
    #     print json.dumps(map_id, ensure_ascii=False)
    print pg.updata_one(sql=sql_request, param=param)
    # result01 = pg.query_one_sql(sql_request)
    # travel_record = result01.get("travel_record", [])
    # occupationdict = result01.get("occupation", {})
    # occupation = occupationdict.get("occupation", u"")
    # print occupation
    # import json
    # print json.dumps(travel_record, ensure_ascii=False, indent=4)
