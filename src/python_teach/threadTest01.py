#!/usr/bin/python3
# -*- coding:utf-8 -*- 
# @Time    : 2018/6/8 16:32
# @Author  : liujiantao
# @Site    : 
# @File    : threadTest01.py
# @Software: PyCharm

import _thread
import time

count = 0
# 为线程定义一个函数
def print_time( threadName, delay):
    global count
    while count < 3:
        # time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
        print ("%s: %d" % ( threadName, count ))

# 创建两个线程
try:
    _thread.start_new_thread( print_time, ("Thread-1", 1, ) )
    _thread.start_new_thread( print_time, ("Thread-2", 2, ) )
    print(count)
except:
    print ("Error: 无法启动线程")

while 1:
    pass
# print(count)