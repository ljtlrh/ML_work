#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/3/14 10:18
# @Author  : liujiantao
# @Site    : 
# @File    : demo01.py
# @Software: PyCharm

import numpy as np

a = np.array([[1,2],[3,4]])
sum0 = np.sum(a, axis=0)
sum1 = np.sum(a, axis=1)

print (sum0)
print (sum1)