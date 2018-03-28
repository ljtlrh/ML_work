#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
对反应企业经营情况的指标进行查询 单元测试
  **GET**：/api/tax/query/operation
'''
import datetime
import requests
import json

if __name__ == '__main__':
    url = "http://127.0.0.1:7000/api/bidding/announceId/company?companyName="
    header = {'Content-Type': 'application/json',
              'sc-id': 'web-1e706182-bb60-430a-8438-ed9e90b5f2a7',
              'sc-mode': 'PRODUCTION',
              'sc-product': 'xx-tools',
              'sc-timer': 'false'}

    params = [
        "顾地科技股份有限公司",
         ]

    for param in params:
        start = datetime.datetime.now()
        result = requests.get(url + param, headers=header)
        data = result.json()
        print(json.dumps(data, ensure_ascii=False, default=lambda x: x.__dict__))
        print("cost time =>" + str(datetime.datetime.now() - start))