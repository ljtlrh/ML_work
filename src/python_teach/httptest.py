#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
对反应企业经营情况的指标进行查询 单元测试
  **GET**：/api/tax/query/operation
'''
import requests
import json
if __name__ == '__main__':
    url = "http://192.168.31.121:9006/api/trademark/summary?companyName="
    header = {'Content-Type': 'application/json',
              'sc-id': 'web-1e706182-bb60-430a-8438-ed9e90b5f2a7',
              'sc-mode': 'PRODUCTION',
              'sc-product': 'xx-tools',
              'sc-timer': 'false'}

    params = "小米科技有限责任公司&from=2015-01-01&to=2018-03-01"

    result = requests.get(url + params, headers=header)
    data = result.json()
    idsList = data.get('data').get('idsList')
    idsList = [item.get('id') for item in idsList]
    print(result.json())