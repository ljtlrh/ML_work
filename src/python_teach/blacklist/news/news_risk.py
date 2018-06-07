# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import sys
import os

from conf.data_conf import STRAT_IP, NEWS_INFO, NEWS_NULL_REQUEST

from src.python_teach.blacklist.blacklistSource import Blacklist

sys.path.append('../..')
sys.path.append('..')
import json
from scpy.logger import get_logger
import requests
from datetime import datetime
from news_analysis import new_strategy_types, checkContent
from multiprocessing.dummy import Pool as ThreadPool

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)
if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'
#
# 合作经营 	投资融资
# 成果奖项 	股权变动
# 产品信息 	违法涉诉
# 重大交易 	债务抵押
# 收购重组 	业务变动
# 高管变动 	员工情况
# 亏损盈利 	安全事故
# 公司信息 	相关提及

NEWS_RISK_LABELS = [u"违法涉诉", u"债务抵押", u"安全事故"]

import boto3
from scpy.xawesome_codechecker import get_ip
import base64

S3 = boto3.resource('s3')

if get_ip().startswith('172.16') or get_ip().startswith('192.168') or get_ip().startswith('127.0.'):
	STRAT_IP = '52.80.91.161:7000'
else:
	STRAT_IP = '172.31.8.30:7000'


def remove_duplicates_in_old_company_name(company_name, old_company_names):
	# 如果为空列表，直接返回
	if old_company_names == []:
		return old_company_names
	# 公司名字去重
	old_company_names = list(set(old_company_names))
	res = []
	# 去除曾用名字中可能为原公司名字的
	for name in old_company_names:
		if name == company_name:
			continue
		else:
			res.append(name)
	return res


class newsBlacklist(Blacklist):
	def __init__(self, company_name, news_count=200):
		super(newsBlacklist, self).__init__()
		if not isinstance(company_name, dict):
			raise TypeError('The input company_name should be a dict, %s obtained' % type(company_name))
		# 公司名字
		self.current_company_name = company_name.get('companyName')
		# 公司曾用名
		self.old_company_name = remove_duplicates_in_old_company_name(company_name=self.current_company_name,
		                                                              old_company_names=company_name.get(
			                                                              'oldCompanyName', []))
		self.news_count = news_count
		# self.pg_news = pg_news
		# self.model = model
		# if not self.pg_news:
		# 	logger.info('connecting news api')
		# 	self.pg_news = PgUtil(database='news', user='wwj', password='1qaz2wsx',
		# 	                      host='sc-news.cfdjbes8ghlt.rds.cn-north-1.amazonaws.com.cn', port='5432')

		self.company_news_info = []

		self.news_bucket = S3.Bucket("search-key-news")

		self.results = {
			'time': str(datetime.now()),  # 当前时间
			'source': u'news',
			'name': u'风险新闻',
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

	def get_news_basic_info_from_db(self, company_name, limit=500):
		'''
		获取一个公司的新闻基本信息，为获取正文做准备，　此处是读库的方式
		:return:
		'''
		logger.info('obtaining news from pg news')
		sql = ''' select url, title, published_time, sc_id, create_ts from news where company_name = \'%s\' order by published_time limit %s ''' \
		      % (company_name, limit)
		news_info = self.pg_news.query_all_sql(sql)
		logger.info('%s news obtained.' % len(news_info))
		if not news_info:
			return None
		if len(news_info) == limit:
			logger.warn('The number of news for company %s exceeded limit %s, only top %s will be kept.' % (
				company_name, limit, limit))
		return news_info

	def get_news_basic_info_from_api(self, company_name):
		'''
		获取一个公司的新闻基本信息，为获取正文做准备，　此处是读库的方式
		:return:
		'''
		headers = {
			"Content-Type": "version=2.0"
		}
		r = requests.get(url='http://%s/api/news/company' % NEWS_INFO, params={'name': company_name}, headers=headers)
		res = r.json() if r.ok else None
		# print res.get("data").get("totalCount")
		res = res.get("data").get("result")

		return res

	def get_news_risk_dict(self, data, company_name):
		'''
		寻找风险新闻的标签
		:param data:
		:param company_name:
		:return:
		'''
		if isinstance(data, dict):
			if data.get("label") in NEWS_RISK_LABELS:
				return {"id": "", "company_name": company_name, "news_id": "", "sc_id": data.get("scId"),
				        "url": data.get("url"),
				        "title": data.get("title"), "hit_results": [], "published_time": data.get("publishTime")}
		return None

	def content_analysis_by_rules(self, id, company_name, url, create_ts, title,
	                              published_time,
	                              sc_id, strategy_keys):
		'''
		新闻内容解析策略，先通过s3获取正文，然后解析
		:param id:
		:param company_name:
		:param url:
		:param create_ts:
		:param title:
		:param published_time:
		:param sc_id:
		:param strategy_keys:
		:return:
		'''
		res = {'news_id': id, 'company_name': company_name, 'sc_id': sc_id, 'url': url, 'news_create_ts': create_ts,
		       'title': title,
		       'published_time': published_time,
		       'hit_results': []}
		try:
			create_ts = str(create_ts).split(' ')[0].replace('-', '/')
			obj = self.news_bucket.Object("text/%s/%s.text" % (create_ts, base64.b64encode(url)))
			content = obj.get()["Body"].read()
			if not content:
				return None
			strategies = new_strategy_types(strategy_keys)
			temp = checkContent(url=sc_id, content=content.decode('utf-8'),
			                    strategies=strategies)
			if temp['hit']:
				res['hit_results'] = json.dumps(temp['hitResults'], ensure_ascii=False)
				return res
		except Exception as e:
			logger.error(e)
		return None

	def send_null_request(self, company_name):
		'''
		请求hotnews
		:param company_name:
		:return:
		'''
		try:
			# para = {'companyName': company_name, 'companyType': 2}
			# 不加companyType=2, 热点新闻只进行全名称匹配
			para = {'companyName': company_name}
			_ = requests.get(NEWS_NULL_REQUEST, params=para)
		except Exception, e:
			pass

	def get_risk_info_from_news_api(self, company_name, scIds=[]):
		'''
		从news的爬虫api获取新闻，如果返回的是带标签的新闻，则直接取负面标签，否则基于规则rule based去解析新闻内容
		:param company_name:
		:param scIds:
		:return:
		'''
		headers = {
			"Content-Type": "version=2.0"
		}
		final_results = []
		page_size = self.news_count
		page_no = 1
		# http://52.80.91.161:18088/api/news/company?name=重庆誉存大数据科技有限公司
		try:
			# 申请更新hotnews，这一步是必须的
			# logger.info('sending null request')
			self.send_null_request(company_name)
			# logger.info('sending null request done')
			# 获取爬取策略
			# logger.info('getting strategy ')
			news_url = 'http://%s/api/news/strategy' % STRAT_IP
			r = requests.get(news_url, params={'name': company_name})
			# logger.info('getting strategy done')
			logger.info("sending request to: " +  news_url + "?name=" + company_name)
			strategies = r.json() if r.ok else {}
			# 获取新闻基本信息
			# logger.info('start getting news')
			basic_news_url = 'http://%s/api/news/company' % NEWS_INFO
			r = requests.get(url=basic_news_url,
			                 params={'name': company_name, 'pageSize': page_size, 'pageNo': page_no},
			                 headers=headers)
			logger.info("sending request to: " + basic_news_url + "?name=" + company_name+"&pageSize="+str(page_size)
						+"&pageNo="+str(page_no))
			logger.info("sending requests to %s get news for %s, (only take %s page(s) with page size %s)" % (
			NEWS_INFO, company_name, page_no, page_size))
			# logger.info('getting news done')
			res = r.json() if r.ok else None
			if res:
				res = res.get("data", {}).get("result", [])
				# 多线程方式实现新闻解析服务
				if res:
					pool = ThreadPool(10)
					jobs = [(company_name, final_results, item, strategies) for item in res]
					pool.map(self.multi_run_wrapper, jobs)
					pool.close()
				pool.join()
		except Exception, e:
			logger.error(e)
		final_results = filter(lambda x: x is not None, final_results)
		# logger.info('analyzing done')
		return final_results

	def multi_run_wrapper(self, args):
		return self.news_content_process(*args)

	def news_content_process(self, company_name, final_results, item, strategies):
		try:
			# 通过返回数据的label字段判断是link否已经标记为风险新闻
			risk_label = self.get_news_risk_dict(item, company_name)
			# 如果未标记为风险新闻，则用规则进行进一步解析
			if not risk_label:
				rule_based_risk = self.content_analysis_by_rules(id='', company_name=company_name,
				                                                 url=item.get('url'),
				                                                 create_ts=item.get('createTs'),
				                                                 title=item.get('title'),
				                                                 published_time=item.get('publishTime'),
				                                                 sc_id=item.get('scId'),
				                                                 strategy_keys=strategies)
				if rule_based_risk:
					final_results.append(rule_based_risk)
			else:
				final_results.append(risk_label)
		except Exception, e:
			logger.error(e)

	def find_risk_news(self):
		'''
		从新闻分析的结果库直接读取
		:param table:
		:return:
		'''
		num_risk_news = 0
		content_res = []
		company_news_info = self.get_company_info_by_name(company_name=self.current_company_name)
		# 处理曾用名的公司名字
		for old_name in self.old_company_name:
			company_news_info.extend(self.get_company_info_by_name(company_name=old_name, name_type=u"old"))

		company_news_info_sorted = sorted(company_news_info, key=lambda k: k['published_time'], reverse=True)
		date_keys = []
		for item in company_news_info_sorted:
			id = item.get('sc_id')
			title = item.get('title').decode('utf-8')
			published_time = item.get('published_time')
			try:
				date_key = str(published_time).split('-')[0]
				content_part = {"type": u"风险新闻", "detail": {}, "companyName": item.get('company_name'),
				                "companyNameType": item.get("companyNameType")}
				content_part['detail']["newsTitle"] = title.decode('utf-8')
				content_part['detail']["newsTime"] = str(published_time).split(' ')[0]
				content_part['detail']["scId"] = id
				# logger.info(item.get('hit_results'))
				if date_key in date_keys:
					for f in content_res:
						if f.get('dateKey') == date_key:
							f['contentPart'].append(content_part)
							f['cnt'] += 1
							break
				else:
					content_res.append({'dateKey': date_key, 'cnt': 1, 'contentPart': [content_part]})
					date_keys.append(date_key)
				num_risk_news += 1
			except Exception, e:
				logger.error(e)
		logger.info('%s risk news found for company %s' % (num_risk_news, self.current_company_name))
		return content_res, num_risk_news

	def get_company_info_by_name(self, company_name, name_type=u'current', merge=True):
		'''
		name type 决定是否为曾用名
		:param company_name:
		:param table:
		:param name_type:
		:return:
		'''
		company_news_info = []
		if self.use_cache:
			company_news_info = self.read_from_cache(company_name, cls='news')
			if company_news_info:
				company_news_info = json.loads(company_news_info)
		if company_news_info is None or not self.use_cache:
			# 取消从新闻库读取的方式
			# sql = ''' select id, company_name, news_id, sc_id, url, title, hit_results, published_time from %s where company_name = \'%s\' and status = 1 ''' \
			#       % (table, company_name)
			# company_news_info = self.pg_news.query_all_sql(sql)
			# 将数据库和url请求过来的新闻合并（只包含风险的新闻）,需要去重
			if merge:
				# company_news_info必须为list, 且已有sc_id. 第一次读redis时,company_news_info为None
				if isinstance(company_news_info, list):
					scIds = [item.get("sc_id") for item in company_news_info]
				else:
					scIds = []
					company_news_info = []
				company_news_info.extend(self.get_risk_info_from_news_api(company_name, scIds=scIds))
			if not company_news_info:
				logger.info('No risk news found for company %s' % company_name)
			self.save_to_cache(company_name=company_name, data=json.dumps(company_news_info), cls='news')
		# 增加companyNameType字段
		company_news_info_new = []
		for item in company_news_info:
			item.update({"companyNameType": name_type})
			company_news_info_new.append(item)
		return company_news_info_new

	def get_results(self):
		'''
		解析新闻内容，　返回结果需满足格式要求
		:return:
		'''
		res, num_risk_news = self.find_risk_news()
		if num_risk_news > 0:
			self.results['count'] = num_risk_news
			self.results['content'] = res
		return self.results


if __name__ == "__main__":
	# pg_news = PgUtil(database='news', user='wwj', password='1qaz2wsx',
	#                  host='sc-news.cfdjbes8ghlt.rds.cn-north-1.amazonaws.com.cn', port='5432')
	# logger.info('connect to news aws db done. ')
	company_name = u'珠海格力电器股份有限公司'
	# company_name = u'五矿发展股份有限公司'
	# company_name = u'辽宁辉山乳业集团叶茂台牧业有限公司'
	company_name = u'万向集团公司'
	company_name = u'广东大洋铝业金属制品有限公司'
	# company_name = u'万向集团公司2'
	company_name = {
		"companyName": u"浙江核新同花顺网络信息股份有限公司",
		# "oldCompanyName": [u"深圳市同洲电子股份有限公司", u"浙富控股集团股份有限公司"],
		"oldCompanyName": []

	}
	n = newsBlacklist(company_name=company_name)
	n.set_cache(False)
	results = n.get_results()
	print json.dumps(results, ensure_ascii=False, indent=2)
