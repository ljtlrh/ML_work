#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: graph_network_demo.py
@time: 18-3-30 上午10:55
"""
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):

    # extract nodes from graph

    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph

    G=nx.Graph()

    # add nodes

    for node in nodes:

        G.add_node(node)


    # add edges

    for edge in graph:

        G.add_edge(edge[0], edge[1])


    # draw graph

    pos = nx.shell_layout(G)

    nx.draw(G, pos)


    # show graph

    plt.show()


# draw example
if __name__ == '__main__':
    graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]

    draw_graph(graph)
