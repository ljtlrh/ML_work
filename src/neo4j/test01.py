#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/6/19 14:40
# @Author  : liujiantao
# @Site    : 
# @File    : test01.py
# @Software: PyCharm
from py2neo import Graph, Path, Node, Relationship

#1. 连接Neo4j
test_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="ljt"
)
#  2.节点的建立 建立节点的时候要定义它的节点标签（label）以及一些基本属性（property）
test_node_1 = Node(label = "Person",name = "test_node_1")
test_node_2 = Node(label = "Person",name = "test_node_2")
test_graph.create(test_node_1)
test_graph.create(test_node_2)

# 3.节点关系的建立
node_1_call_node_2 = Relationship(test_node_1,'CALL',test_node_2)
node_1_call_node_2['count'] = 1
node_2_call_node_1 = Relationship(test_node_2,'CALL',test_node_1)
node_2_call_node_1['count'] = 2
test_graph.create(node_1_call_node_2)
test_graph.create(node_2_call_node_1)
# 如果建立关系的时候，起始节点或者结束节点不存在，则在建立关系的同时建立这个节点。
# 4.更新关系或节点的属性
node_1_call_node_2['count']+=1
test_graph.push(node_1_call_node_2)  # 将更新的关系或节点push提交
# 5.通过属性值来查找节点和关系
# 通过find和find_one函数，可以根据类型和属性、属性值来查找节点和关系。
# 示例如下：

find_code_1 = test_graph.find_one(
  label="Person",
  property_key="name",
  property_value="test_node_1"
)
print (find_code_1['name'])
find_code_2 = test_graph.find_one(
  label="Person",
  property_key="name",
  property_value="test_node_2"
)
print (find_code_2['name'])

# find和find_one的区别在于：
# find_one的返回结果是一个具体的节点/关系，可以直接查看它的属性和值。如果没有这个节点/关系，返回None。
# find查找的结果是一个游标，可以通过循环取到所找到的所有节点/关系。
# 6.通过节点/关系查找相关联的节点/关系
find_relationship = test_graph.match_one(start_node=find_code_1,end_node=find_code_2,bidirectional=False)
print (find_relationship)

# bidirectional参数的意义是指关系是否可以双向。
# 如果为False,则起始节点必须为start_node，结束节点必须为end_node。如果有Relationship参数，则一定按照Relationship对应的方向。
# 如果为True，则不需要关心方向问题，会把两个方向的数据都返回。

