#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: handler_helper.py
@time: 18-4-26 下午5:47
"""
import datetime
import tornado

from src.pysaprk_demo.monitor_hadoop.monitor_get_data import MonitorGetData

md = MonitorGetData()


class APIMonitorHandler(tornado.web.RequestHandler):
    """
    API 访问情况监控, 包括
    1、访问记录
    2、最近访问接口
    3、接口访问频率、时间分布
    """
    _ACTION_CHOICE = ["AccessLogs", "RecentAccess", "AccessFrequency"]

    def get(self, *args, **kwargs):
        heap_memory = md.GetHeapMemory()
        fsn_name_system_state = md.FSNamesystemState()
        self.render("../templates/index.html",
                    last_success_request=heap_memory,
                    last_fail_request=fsn_name_system_state)
