#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-6 上午10:51
# @Author  : liujiantao
# @Site    : 
# @File    : threadsutils.py
# @Software: PyCharm
import sys
import threading
import Queue
import time
import copy
from multiprocessing.dummy import Pool as ThreadPool

class ThreadPoolUtils(object):
    '''
    多线程工具类
    '''

    def __init__(self, thread_num):
        self.NUMBER_OF_THREADS = thread_num
        self.work_queue = Queue.Queue()
        self.threads = []
        self.all_list = []
        self.data_network = {}
        # self.__init_work_queue(fun_number)
        # self.__init_thread_pool(thread_num)

    """
        initialize threads
    """

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(MyThread(self.work_queue))

    """
        initialize work queue
    """

    def __init_work_queue(self, fun_number):
        for i in range(fun_number):
            self.add_job(do_job)

    """
    		add a job to the queue
    	"""

    def add_job(self, func, args):
        self.work_queue.put((func, args))

    """
        wait for all the threads to be completed
    """

    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()

    def threading(self, functionName_list, company_name):
        # start NUMBER_OF_THREADS pool
        pool = ThreadPool(self.NUMBER_OF_THREADS)
        for fun in functionName_list:
            pool.map(fun, company_name)
        # 关闭线程池（对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()
        pool.close()
        # 加入子进程执行（使得子进程运行结束后再执行父进程
        pool.join()
        # 从队列恢复数据为dict,
        while self.work_queue.qsize() != 0:
            temp = self.work_queue.get()
            self.data_network[temp.get("functionName")] = temp.get("data")
        return self.data_network

class MyThread(threading.Thread):
	def __init__(self, work_queue):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
		self.start()

	def run(self):
		while True:
			try:
				do, args = self.work_queue.get(block=False)
				do(args)
				self.work_queue.task_done()#notify the completement of the job
			except:
				break

ERROR_NUM = 0

def do_job(args):
	try:
		# html = urllib2.urlopen(args)
		print ("args:"+str(args))
	except Exception as e:
		global ERROR_NUM
		ERROR_NUM += 1


def fun1(company_name):
    print ("fun1")
    tp.work_queue.put({"functionName": "fun1", "data": "1254"})


def fun2(company_name):
    print ("fun2")
    tp.work_queue.put({"functionName": "fun2", "data": "48564"})


def fun3(company_name):
    print ("fun3")
    tp.work_queue.put({"functionName": "fun3", "data": "1546"})

if __name__ == '__main__':

    import datetime
    t1 = datetime.datetime.now()
    tp = ThreadPoolUtils(3)
    functionName_list = [fun1, fun2, fun3]
    all_list = tp.threading(functionName_list=functionName_list, company_name="1111")
    # tp.wait_all_complete()
    print (all_list)
    print ("COST TIME:"+str(datetime.datetime.now()-t1))