#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: one_hot_encoding.py
@time: 18-5-3 上午10:48
"""
import pandas as pd
file_path = "/home/sinly/ljtstudy/back/new_version_all_features.csv"
feature_name = ["industry", "province", "regcap", "zczjbz"]
df = pd.read_csv(file_path)
data = list(set(df['industry'].tolist()))
del df
one_hot = pd.get_dummies(data)
print(one_hot.head(10))
