# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import sys
import os

from blacklist_sources.news.news_content import newsContent
from conf.data_conf import STRAT_IP, NEWS_INFO, NEWS_MODE_READ_DB, NUMBER_OF_THREADS

sys.path.append('../..')
sys.path.append('..')
import json
from scpy.logger import get_logger
from  utils.pgutil import PgUtil
from  blacklist_sources.blacklistSource import Blacklist
import requests
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)
if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'

NEWS_RISK_LABELS = [u"违法涉诉", u"债务抵押", u"安全事故"]


class newsBlacklistNetwork(Blacklist):
	def __init__(self, company_names, pg_news=None, model=NEWS_MODE_READ_DB):
		super(newsBlacklistNetwork, self).__init__()
		if not isinstance(company_names, list):
			raise TypeError('The input for company should be a list')
		self.model = model
		self.company_names = company_names
		self.pg_news = pg_news

		if not self.pg_news:
			logger.info('connecting news api')
			self.pg_news = PgUtil(database='news', user='wwj', password='1qaz2wsx',
			                      host='sc-news.cfdjbes8ghlt.rds.cn-north-1.amazonaws.com.cn', port='5432')

		self.company_news_info = []

		self.results = {
			'time': str(datetime.now()),  # 当前时间
			'source': u'connectNews',
			'name': u'关联公司-风险新闻',
			'count': 0,
			'scIds': [],
			'content': []
		}

	def __get_strategy(self, company_name):
		'''
		获取新闻爬取策略
		:param company_name:
		:return:
		'''
		r = requests.get('http://%s/api/news/strategy' % STRAT_IP, params={'name': company_name})
		res = r.json() if r.ok else {}
		return res

	def get_news_risk_dict(self, data, company_name):
		if isinstance(data, dict):
			if data.get("label") in NEWS_RISK_LABELS:
				return {"id": "", "company_name": company_name, "news_id": "", "sc_id": data.get("scId"),
				        "url": data.get("url"),
				        "title": data.get("title"), "hit_results": [], "published_time": data.get("publishTime")}
		return None

	def get_risk_news_from_url(self, company_name, scIds=[]):

		headers = {
			"Content-Type": "version=2.0"
		}
		final_results = []
		# http://52.80.91.161:18088/api/news/company?name=重庆誉存大数据科技有限公司
		try:
			r = requests.get(url='http://%s/api/news/company' % NEWS_INFO, params={'name': company_name},
			                 headers=headers)
			logger.info("sending requests to %s get news for %s" % (NEWS_INFO, company_name))
			res = r.json() if r.ok else None
			# id, company_name, news_id, sc_id, url, title, hit_results, published_time
			if res:
				res = res.get("data", {}).get("result", [])
				final_results_temp = [
					self.get_news_risk_dict(item, company_name) if item.get("scId") not in scIds else None for item in
					res]
				# 去None
				final_results = filter(lambda x: x is not None, final_results_temp)
		except Exception, e:
			logger.error(e)
		return final_results

	def get_news_basic_info_from_db(self, company_name, limit=50):
		'''
		获取一个公司的新闻基本信息，为获取正文做准备，　此处是读库的方式
		:return:
		'''
		# 获取网络图的公司中最新的50条新闻
		sql = ''' select url, title, published_time, sc_id, create_ts from news where company_name = \'%s\' order by published_time desc limit %s ''' \
		      % (company_name, limit)

		news_info = self.pg_news.query_all_sql(sql)

		logger.info('%s news obtained for company %s.' % (len(news_info), company_name))
		if not news_info:
			self.company_info_queue.put({'companyName': company_name, 'data': None})
			return None
		if len(news_info) == limit:
			logger.warn('The number of news for company %s exceeded limit %s, only top %s will be kept.' % (
				company_name, limit, limit))
		self.company_info_queue.put({'companyName': company_name, 'data': news_info})

	def get_news_basic_info_from_api(self, company_name):
		'''
		获取一个公司的新闻基本信息，为获取正文做准备
		:return:
		'''
		headers = {
			"Content-Type": "version=2.0"
		}
		r = requests.get(url='http://%s/api/news/company' % NEWS_INFO, params={'name': company_name}, headers=headers)
		res = r.json() if r.ok else None
		res = res.get("data").get("result")

		return res

	def get_all_company_news(self):
		'''
		多线程获取公司新闻数据
		:return:
		'''
		pool = ThreadPool(NUMBER_OF_THREADS)
		company_list = newsBlacklistNetwork.get_company_names_from_network(network_data=self.company_names)
		pool.map(self.get_news_basic_info_from_db, company_list)
		pool.close()
		pool.join()
		# 从队列恢复数据为dict, 以公司名字作为主键
		while self.company_info_queue.qsize() != 0:
			temp = self.company_info_queue.get()
			self.data_network[temp.get('companyName')] = temp.get('data')

		# 恢复格式
		for item in self.company_names:
			data_info = self.data_network[item.get('companyName')]
			res = {'news': data_info, 'companyName': item.get('companyName'), 'connectType': item.get('connectType')}
			self.company_news_info.append(res)

	def find_news_risk_from_db(self):
		'''
		从新闻分析的结果库直接读取网络图的数据
		:param table:
		:return:
		'''
		num_comp_has_risk = 0
		final_res = []

		pool = ThreadPool(NUMBER_OF_THREADS)
		company_list = newsBlacklistNetwork.get_company_names_from_network(network_data=self.company_names)
		pool.map(self.get_risk_news_by_company_name, company_list)
		pool.close()
		pool.join()
		# 从队列恢复数据为dict, 以公司名字作为主键
		while self.company_info_queue.qsize() != 0:
			temp = self.company_info_queue.get()
			self.data_network[temp.get('companyName')] = temp.get('data')

		for item in self.company_names:
			num_risk_news = 0
			company_name = item.get('companyName').decode('utf-8')
			connect_type = item.get('connectType').decode('utf-8')
			company_news_info = self.data_network[company_name]

			company_res = {'companyName': company_name, 'connectType': connect_type, 'cnt': 0, 'contentPart': []}
			for item2 in company_news_info:
				id = item2.get('sc_id')
				title = item2.get('title').decode('utf-8')
				published_time = item2.get('published_time')
				try:
					content_part = {"type": u"风险新闻", "detail": {}}
					content_part['detail']["newsTitle"] = title.decode('utf-8')
					content_part['detail']["newsTime"] = str(published_time).split(' ')[0]
					content_part['detail']["scId"] = id
					# logger.info(item2.get('hit_results'))
					num_risk_news += 1
					company_res['contentPart'].append(content_part)
				except Exception, e:
					logger.error(e)
			# 时间排序
			if company_res['contentPart']:
				company_res['contentPart'].sort(key=lambda e: e['detail']['newsTime'], reverse=True)

			if num_risk_news >= 1:
				company_res['cnt'] = num_risk_news
				final_res.append(company_res)
				num_comp_has_risk += 1
		return final_res, num_comp_has_risk

	def get_risk_news_by_company_name(self, company_name, merge=True):
		company_news_info = []
		data_info_in_cache = None
		if self.use_cache:
			data_info_in_cache = self.read_from_cache(company_name=company_name, cls='news')
			if data_info_in_cache:
				company_news_info = json.loads(data_info_in_cache)
		if not self.use_cache or data_info_in_cache is None:
			sql = ''' select id, company_name, news_id, sc_id, url, title, hit_results, published_time from news_analysis where company_name = \'%s\' and status = 1 ''' \
			      % (company_name)
			company_news_info = self.pg_news.query_all_sql(sql)
			# 将数据库和url请求过来的新闻合并（只包含风险的新闻）,需要去重
			if merge:
				# 已有的sc_id
				scIds = [item.get("sc_id") for item in company_news_info]
				company_news_info.extend(self.get_risk_news_from_url(company_name, scIds=scIds))
			if not company_news_info:
				logger.info('No risk news found for company %s' % company_name)
				# 如果未获取到，存空list
				company_news_info = []
			self.save_to_cache(company_name=company_name, data=json.dumps(company_news_info), cls='news')
		self.company_info_queue.put({'companyName': company_name, 'data': company_news_info})

	def find_news_risk_online(self):
		'''
		调用新闻分析api，　分析新闻中风险信息
		:return:
		'''
		num_comp_has_risk = 0
		final_res = []
		logger.info('loading news for companies via multi-process')
		self.get_all_company_news()
		n = newsContent()
		for company_info in self.company_news_info:
			company_name = company_info.get('companyName').decode('utf-8')
			connect_type = company_info.get('connectType').decode('utf-8')
			news_info = company_info.get('news')
			if not news_info:
				logger.info('There is no news found for company %s' % self.company_names)
				continue
			strategy_keys = self.__get_strategy(company_name)
			n.set_input_data(input_data=news_info)
			n.set_strategy(strategy=strategy_keys)
			news_info_analyzed = n.get_all_news_content()
			num_risk_news = 0
			company_res = {'companyName': company_name, 'connectType': connect_type, 'cnt': 0, 'contentPart': []}
			for item in news_info_analyzed:
				id = item.get('sc_id')
				title = item.get('title').decode('utf-8')
				published_time = item.get('published_time')
				content = item.get('content')
				if company_name and id and content:
					try:
						if item.get('news_analysis_results').get('hit'):
							content_part = {"type": u"风险新闻", "detail": {}}
							content_part['detail']["newsTitle"] = title.decode('utf-8')
							content_part['detail']["newsTime"] = str(published_time).split(' ')[0]
							content_part['detail']["scId"] = id
							logger.info(
								json.dumps(item.get('news_analysis_results').get('hitResults'), ensure_ascii=False))
							num_risk_news += 1
							company_res['contentPart'].append(content_part)
					except Exception, e:
						logger.error(e)
			# 时间排序
			if company_res['contentPart']:
				company_res['contentPart'] = company_res['contentPart'].sort(key=lambda e: e['detail']['newsTime'],
				                                                             reverse=True)
			if num_risk_news >= 1:
				company_res['cnt'] = num_risk_news
				final_res.append(company_res)
				num_comp_has_risk += 1

			logger.info('%s risk news found for company %s' % (num_comp_has_risk, company_name))
		return final_res, num_comp_has_risk

	def get_results(self):
		'''
		解析新闻内容，　返回结果需满足格式要求
		:return:
		'''

		if self.model == NEWS_MODE_READ_DB:
			res, num_comp_has_risk = self.find_news_risk_from_db()
		else:
			res, num_comp_has_risk = self.find_news_risk_online()
		self.results['count'] = num_comp_has_risk
		res_sorted = sorted(res, key=lambda x: x['cnt'], reverse=True)
		self.results['content'] = res_sorted
		return self.results


if __name__ == "__main__":
	pg_news = PgUtil(database='news', user='wwj', password='1qaz2wsx',
	                 host='sc-news.cfdjbes8ghlt.rds.cn-north-1.amazonaws.com.cn', port='5432')
	# company_name = u'珠海格力电器股份有限公司'
	company_names = [
		{'companyName': u'万向集团公司', 'connectType': u'对外投资'},
		{'companyName': u'上海大智慧股份有限公司', 'connectType': u'对外投资'},
		{'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司', 'connectType': u'对外投资'},
		# {'companyName': u'五矿发展股份有限公司2', 'connectType': u'对外投资'},
	]
	# company_names = [
	# 	{"companyName": u"上海大智慧股份有限公司", "connectType": u"对外投资"},
	# 	{"companyName": u"万向集团公司", "connectType": u"对外投资"},
	# 	{"companyName": u"五矿发展股份有限公司", "connectType": u"对外投资"}
	# ]
	n = newsBlacklistNetwork(company_names=company_names, pg_news=pg_news)
	# n.get_all_company_news()
	# print n.company_news_info
	n.set_cache(False)
	results = n.get_results()
	print json.dumps(results, ensure_ascii=False, indent=2)
