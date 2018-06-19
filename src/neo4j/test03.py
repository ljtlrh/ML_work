#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/6/19 15:16
# @Author  : liujiantao
# @Site    : 
# @File    : test03.py
# @Software: PyCharm


import pymysql
from neo4j.v1 import GraphDatabase


uri = "http://localhost:7474"
driver = GraphDatabase.driver(uri, auth=("neo4j", "ljt"))


print("先删除所有节点和关系")
with driver.session() as session:
    session.write_transaction(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))


print("检查是否为空")
with driver.session() as session:
    session.write_transaction(lambda tx: tx.run('MATCH (n) RETURN n'))


conn = pymysql.connect(host='xxxxdb.mysql.rds.aliyuncs.com',
                       port=3306, user='userxxx', passwd='pswdxxxx',
                       db='ust', charset='utf8')
c_t = conn.cursor()
sql = 'select query_idcard, query_mobile, query_name, query_bankcard ' \
      'from id34_record ' \
      'where result_code=\'00\' or result_code=\'000\';'
c_t.execute(sql)
r_t = c_t.fetchall()
nnn = 0
for i in r_t:
    # print(i)
    if i[0] == None or i[1] == None or i[2] == None or i[3] == None:
        #暂时不考虑三要素
        continue


    if (nnn % 100 == 0):
        print('-'*10)
        print(nnn)
    # print(nnn)
    nnn += 1


    id = i[0]
    mp = i[1]
    name = i[2] #暂时不考虑姓名
    bankcard = i[3]


    #不重复地创建节点
    node_type = 'MP'
    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run("MERGE (:MP {val:$val})", {'val':mp}))
    node_type = 'ID'
    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run("MERGE (:ID {val:$val})", {'val':id}))


    node_type = 'BANKCARD'
    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run("MERGE (:BANKCARD {val:$val})", {'val':bankcard}))


    #创建关系
    cmd = "MATCH (n:MP) WHERE n.val=\"%s\" \n" \
          "MATCH (m:ID) WHERE m.val=\"%s\" \n" \
          "MATCH (p:BANKCARD) WHERE p.val=\"%s\" \n" \
          "MERGE (n)-[:BIND]->(m) \n" \
          "MERGE (m)-[:BIND]->(n) \n" \
          "MERGE (n)-[:BIND]->(p) \n" \
          "MERGE (p)-[:BIND]->(n) \n" \
          "MERGE (m)-[:BIND]->(p) \n" \
          "MERGE (p)-[:BIND]->(m) \n" \
          %(mp, id, bankcard)
    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run(cmd))
