#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/4/27 20:40
# @Author  : liujiantao
# @Site    : ${SITE}
# @File    : test_monitorGetData.py
import json
from unittest import TestCase

from ML_work.src.pysaprk_demo.monitor_hadoop.monitor_get_data import MonitorGetData

md = MonitorGetData()


# @Software: PyCharm
def my_print(*input_str):
    print(json.dumps(input_str, ensure_ascii=False, indent=4, default=lambda x: str(x)))


class TestMonitorGetData(TestCase):

    def test_GetHeapMemory(self):
        res = md.GetHeapMemory()
        my_print(res)

    def test_FSNamesystemState(self):
        res = md.FSNamesystemState()
        my_print(res)

    def test_NameNodeInfo(self):
        res = md.NameNodeInfo()
        my_print(res)

    def test_HadoopResourceManager(self):
        res = md.HadoopResourceManager()
        my_print(res)
