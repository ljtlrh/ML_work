#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-5 下午5:49
# @Author  : liujiantao
# @Site    : 
# @File    : ThreadPoolTest.py
# @Software: PyCharm
#coding:gbk

"""
模拟apache benchmark的一个简单的网站压力测试程序，用python编写，可以自由选择发送请求数以及并发的线程数
使用示例：

$ python problem2.py -n 100 -c 10 -u http://www.163.com
URL: http://www.163.com Total Requests Number: 100 Concurrent Requests Number: 10 Total Time Cost(seconds): 21.3480730057 Average Time Per Request: 0.213480730057 Average Requests Number Per Second: 4.68426353861 Total Error Number: 0
"""

import sys
import threading
import Queue
import time
from optparse import OptionParser

class ThreadPool(object):
	def __init__(self, urlpth, req_number, thread_num):
		self.work_queue = Queue.Queue()
		self.threads = []
		self.__init_work_queue(req_number, urlpth)
		self.__init_thread_pool(thread_num)
	"""
		initialize threads
	"""
	def __init_thread_pool(self, thread_num):
		for i in range(thread_num):
			self.threads.append(MyThread(self.work_queue))

	"""
		initialize work queue
	"""
	def __init_work_queue(self, req_number, urlpth):
		for i in range(req_number):
			self.add_job(do_job, urlpth)

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
	except Exception, e:
		print e
		global ERROR_NUM
		ERROR_NUM += 1


def parse():
	"""parse the args"""
	parser = OptionParser(description="The scripte is used to simulate apache benchmark(sending requests and testing the server)")
	parser.add_option("-n", "--number", dest="num_of_req", action="store", help="Number of requests you want to send", default=1)
	parser.add_option("-c", "--concurrent", dest="con_req", action="store", help="Number of concurrent requests you set", default=1)
	parser.add_option("-u", "--url", dest="urlpth", action="store", help="The url of server you want to send to")
	(options, args) = parser.parse_args()
	return options

def main():
	"""main function"""
	start = time.time()
	options = parse()

	if not options.urlpth:
		print 'Need to specify the parameter option "-u"!'
	if '-h' in sys.argv or '--help' in sys.argv:
		print __doc__

	tp = ThreadPool(options.urlpth, int(options.num_of_req), int(options.con_req))
	tp.wait_all_complete()
	end = time.time()

	print "==============================================="
	print "URL: ", options.urlpth
	print "Total Requests Number: ", options.num_of_req
	print "Concurrent Requests Number: ", options.con_req
	print "Total Time Cost(seconds): ", (end-start)
	print "Average Time Per0 1...." \
		  "00Request: ", (end-start)/int(options.num_of_req)
	print "Average Requests Number Per Second: ", int(options.num_of_req)/(end-start)
	print "Total Error Number: ", ERROR_NUM


if __name__ == '__main__':
	main()
