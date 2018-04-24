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
from multiprocessing import Pool, Process


def f1(name):
    print ('hello', name)


def f(x):
    return x * x

class fff(object):



    def test_pool(self):
        p = Pool(5)
        print(p.map_async(f1, [1, 2, 3]))
        print(p.map_async(f1, [1, 32, 3]))
        print(p.map_async(f, [1, 42, 3]))

    def test_Process(self):
        p1 = Process(target=f1, args=('bob',))
        p2 = Process(target=f1, args=('aaa',))
        p3 = Process(target=f1, args=('sss',))
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    # test_pool()
    fff = fff()
    # fff.test_Process()
    fff.test_pool()
    end = datetime.datetime.now()
    print ("Cost Time:"+str(end - start))