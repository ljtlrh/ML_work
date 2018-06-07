# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import sys
import os

sys.path.append('../..')
sys.path.append('..')
import json
from scpy.logger import get_logger
from  utils.pgutil import PgUtil
from psycopg2.extensions import AsIs
import requests

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)
if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'

import base64

import boto3
from threading import Thread
from blacklist_sources.news.news_analysis import checkContent, new_strategy_types
from scpy.xawesome_codechecker import get_ip
# from multiprocessing.dummy import Pool

if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'

S3 = boto3.resource('s3')
if get_ip().startswith('192.168'):
	STRAT_IP = '52.80.91.161:7000'
else:
	STRAT_IP = '172.31.8.30:7000'

pg_news = PgUtil(database='news', user='wwj', password='1qaz2wsx',
                 host='sc-news.cfdjbes8ghlt.rds.cn-north-1.amazonaws.com.cn', port='5432')

logger.info('connect news db done.')


def save_dict_to_pg_db(pg, data, table='news_analysis', returning_id=False):
	'''
	将一个dict存入指定的数据库, 返回插入成功与否或者id
	:param pg:
	:param data:
	:param db_name:
	:return:
	'''
	if not isinstance(data, dict):
		raise ValueError('The input has to be a dict')

	columns = data.keys()
	values = [data[column] for column in columns]
	id = None
	try:
		if returning_id:
			insert_statement = '''insert into ''' + table + ''' (%s) values %s RETURNING id;'''
			id = pg.execute_insert_sql_with_return_id(insert_statement, (AsIs(','.join(columns)), tuple(values)))
		else:
			insert_statement = '''insert into ''' + table + ''' (%s) values %s ;'''
			pg.execute_insert_sql(insert_statement, (AsIs(','.join(columns)), tuple(values)))
			return True
	except Exception, e:
		logger.error(e)
		return False
	return id


def get_strategy(company_name):
	'''
	获取新闻爬取策略
	:param company_name:
	:return:
	'''
	r = requests.get('http://%s/api/news/strategy' % STRAT_IP, params={'name': company_name})
	res = r.json() if r.ok else {}
	return res


class newsContent(object):
	def __init__(self, input_data=None, strategy_keys=None):
		# self.pool = Pool(processes=PROCESSOR_NUM)
		self.news_bucket = S3.Bucket("search-key-news")
		self.strategy_keys = strategy_keys
		self.input_data = input_data

	def set_input_data(self, input_data):
		self.input_data = input_data

	def set_strategy(self, strategy):
		self.strategy_keys = strategy

	def __get_news_content_and_save(self, id, company_name, url, create_ts, title,
	                                published_time,
	                                sc_id):
		res = {'news_id': id, 'company_name': company_name, 'sc_id': sc_id, 'url': url, 'news_create_ts': create_ts,
		       'title': title,
		       'published_time': published_time,
		       'hit_results': []}
		try:
			create_ts = str(create_ts).split(' ')[0].replace('-', '/')
			obj = self.news_bucket.Object("text/%s/%s.text" % (create_ts, base64.b64encode(url)))
			content = obj.get()["Body"].read()
			if not content:
				return
			# res['content'] = content
			strategies = new_strategy_types(self.strategy_keys)
			temp = checkContent(url=sc_id, content=content.decode('utf-8'),
			                    strategies=strategies)
			if temp['hit']:
				res['hit_results'] = json.dumps(temp['hitResults'], ensure_ascii=False)
				logger.info('saving data for company %s with sc id %s' % (company_name, sc_id))
				save_dict_to_pg_db(pg=pg_news, data=res)

		except Exception as e:
			logger.error(e)
		return True

	def __get_news_content_wrapper(self, kwargs):
		return self.__get_news_content_and_save(**kwargs)

	def save_news_analysis_results(self):
		logger.info('starting obtain news content for %s news by multi-threads' % len(self.input_data))
		threads = []
		for item in self.input_data:
			temp = {'url': item.get('url'),
			        'create_ts': str(item.get('create_ts')),
			        'title': item.get('title'),
			        'published_time': str(item.get('published_time')),
			        'sc_id': item.get('sc_id'),
			        'company_name': item.get('company_name'),
			        'id': item.get('id')
			        }
			threads.append(Thread(target=self.__get_news_content_and_save,
			                      kwargs=temp))
		[x.start() for x in threads]
		[x.join() for x in threads]

		logger.info('obtained news content and analysis done.')


from datetime import datetime, timedelta

REF_DATE = {"hour": 1, "minute": 0, "second": 0, "microsecond": 0}
TASK_DAY_OFFSET = 1


def news_all(pg_news):
	'''
	全量更新新闻分析结果
	:param pg_news:
	:return:
	'''

	sql = ''' select distinct(company_name) from news '''

	company_names = pg_news.query_all_sql(sql)
	# company_names = [{'company_name':u'五矿发展股份有限公司'}]
	logger.info('%s company will be updated' % len(company_names))
	n = newsContent()
	for item in company_names:
		company_name = item.get('company_name').decode('utf-8')
		logger.info('processing company %s' % company_name)
		strategy = get_strategy(company_name)
		sql2 = ''' select id, company_name, url, title, published_time, sc_id, create_ts from news where company_name = \'%s\' ''' % company_name
		data = pg_news.query_all_sql(sql2)
		n.set_strategy(strategy=strategy)
		n.set_input_data(input_data=data)
		n.save_news_analysis_results()
	logger.info('Process done.')


def news_task():
	ref_date = str((datetime.now() - timedelta(days=TASK_DAY_OFFSET)).replace(
		hour=REF_DATE.get("hour", 0), minute=REF_DATE.get("minute"),
		second=REF_DATE.get("second", 0), microsecond=REF_DATE.get("microsecond", 0)))
	logger.info('news create_ts bigger than %s will obtained' % ref_date)
	sql = ''' select distinct(company_name) from news where create_ts >= '%s'; ''' % ref_date
	company_news = pg_news.query_all_sql(sql)
	logger.info('%s company will be updated' % len(company_news))
	n = newsContent()
	for item in company_news:
		company_name = item.get('company_name').decode('utf-8')
		logger.info('processing company %s' % company_name)
		sql2 = ''' select id, company_name, url, title, published_time, sc_id, create_ts from news where company_name = \'%s\' and create_ts >= '%s';''' % \
		       (company_name, ref_date)
		data = pg_news.query_all_sql(sql2)
		strategy = get_strategy(company_name)
		n.set_strategy(strategy=strategy)
		# 一次处理一条新闻
		n.set_input_data(input_data=data)
		n.save_news_analysis_results()
	logger.info('News analysis process done.')


if __name__ == "__main__":
	# news_all(pg_news=pg_news)
	news_task()
