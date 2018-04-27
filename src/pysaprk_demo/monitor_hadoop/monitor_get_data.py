#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: monitor_get_data.py
@time: 18-4-27 下午5:54
"""
import urllib.request as urllib2
import json
import os

# settings section
ZABBIX_NAME = "namenode"
CLUSTER_HOST = "127.0.0.1"


class MonitorGetData(object):

    def get_HeapMemory(self):
        # --------------------------------------------------------------------------------------------
        # HeapMemory
        # --------------------------------------------------------------------------------------------
        HeapMemory = []
        url1 = "http://" + CLUSTER_HOST + ":50070/jmx?qry=java.lang:type=Memory"
        response = urllib2.Request(url1)
        res_data = urllib2.urlopen(response)
        res = res_data.read()
        hjson = json.loads(res.decode())
        heap_memory_committed = round(float(hjson['beans'][0]["HeapMemoryUsage"]["committed"]) / 1024 / 1024, 2)
        heap_memory_init = round(float(hjson['beans'][0]["HeapMemoryUsage"]["init"]) / 1024 / 1024, 2)
        heap_memory_max = round(float(hjson['beans'][0]["HeapMemoryUsage"]["max"]) / 1024 / 1024, 2)
        heap_memory_used = round(float(hjson['beans'][0]["HeapMemoryUsage"]["used"]) / 1024 / 1024, 2)
        nonheap_memory_committed = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["committed"]) / 1024 / 1024, 2)
        nonheap_memory_init = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["init"]) / 1024 / 1024, 2)
        nonheap_memory_max = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["max"]) / 1024 / 1024, 2)
        nonheap_memory_used = round(float(hjson['beans'][0]["NonHeapMemoryUsage"]["used"]) / 1024 / 1024, 2)
        return HeapMemory