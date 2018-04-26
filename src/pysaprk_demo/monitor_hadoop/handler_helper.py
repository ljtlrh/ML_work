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


class APIMonitorHandler(tornado.web.RequestHandler):
    """
    API 访问情况监控, 包括
    1、访问记录
    2、最近访问接口
    3、接口访问频率、时间分布
    """
    _ACTION_CHOICE = ["AccessLogs", "RecentAccess", "AccessFrequency"]

    def get(self, *args, **kwargs):
        last_success_request = get_recent_success_cpcn_request_service()
        last_fail_request = get_recent_fail_cpcn_request_service()

        self.render("../templates/index.html",
                    last_success_request=last_success_request,
                    last_fail_request=last_fail_request)
