#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-7 上午10:18
# @Author  : liujiantao
# @Site    : 
# @File    : multiprocessingUtils.py
# @Software: PyCharm
'''
python2.7 多进程实现多线程功能
see https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing
discription:    multiprocessing is a package that supports spawning processes
using an API similar to the threading module. The multiprocessing
package offers both local and remote concurrency, effectively side-stepping
the Global Interpreter Lock by using subprocesses instead of threads. Due to this,
the multiprocessing module allows the programmer to fully leverage multiple processors on a given machine.
It runs on both Unix and Windows.
'''
from multiprocessing import Pool

def f(x):
    return x*x

from multiprocessing import Process

def f1(name):
    print ('hello', name)

def test_pool():
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))

def test_Process():
    p = Process(target=f1, args=('bob',))
    p.start()
    p.join()
if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    # test_pool()
    test_Process()
    end = datetime.datetime.now()
    print ("Cost Time:"+str(end - start))