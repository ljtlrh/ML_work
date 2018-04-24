#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: net_work01.py
@time: 18-4-16 上午10:43
"""
import networkx as nx
import matplotlib.pyplot as plt
G = nx.complete_graph(5)
K5 = nx.convert_node_labels_to_integers(G,first_label=2)
G.add_edges_from(K5.edges())#对地图中添加边
#G为图，normalized使用随机网络进行规范化，Q（float（可选，默认值= 100）)
# 如果normalized = True通过执行Q * M双边交换创建一个随机网络，其中M是G中的边数，用作归一化的空模型。
rc = nx.rich_club_coefficient(G,normalized=False)
print(rc)#各个节点的富俱乐部系数
nx.draw(G)
plt.show()