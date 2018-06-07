#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 
@site: 
@software: PyCharm
@file: bankrupt_feature_deal.py
@time: 18-5-31 下午4:19
"""
def get_company_names01(path):
    company_names = []
    with open(path) as f:
        for data in f.readlines():
            if data.startswith('#'):
                continue
            name = data.decode('utf-8')
            # print name
            company_names.append(name)
    return company_names

if __name__ == '__main__':
    bankrupt_company = get_company_names01("/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company.txt")
    for company in bankrupt_company:
        pass

