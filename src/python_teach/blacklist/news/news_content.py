# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import os
import base64
from threading import Thread

from scpy.logger import get_logger
import boto3

from blacklist_sources.news.news_analysis import checkContent, new_strategy_types

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)

if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'

S3 = boto3.resource('s3')


class newsContent(object):
	def __init__(self, input_data=None, strategy_keys=None):
		self.news_bucket = S3.Bucket("search-key-news")
		self.contents = []
		self.strategy_keys = strategy_keys
		self.input_data = input_data

	def set_input_data(self, input_data):
		self.input_data = input_data

	def set_strategy(self, strategy):
		self.strategy_keys = strategy

	def __get_news_content(self, url, create_ts, title, published_time, sc_id):
		res = {'url': url, 'create_ts': create_ts, 'content': '', 'title': title, 'published_time': published_time,
		       'sc_id': sc_id, 'news_analysis_results': []}
		try:
			create_ts = str(create_ts).split(' ')[0].replace('-', '/')
			obj = self.news_bucket.Object("text/%s/%s.text" % (create_ts, base64.b64encode(url)))
			content = obj.get()["Body"].read()
			if not content:
				return
			res['content'] = content
			strategies = new_strategy_types(self.strategy_keys)
			res['news_analysis_results'] = checkContent(url=sc_id, content=content.decode('utf-8'),
			                                            strategies=strategies)
		except Exception as e:
			logger.error(e)
			return
		self.contents.append(res)

	def __get_news_content_wrapper(self, kwargs):
		return self.__get_news_content(**kwargs)

	# def get_all_news_content2(self):
	# 	logger.info('starting obtain news content for %s news by multi-processors' % len(self.input_data))
	# 	self.pool.map(self.__get_news_content_wrapper, self.input_data)
	# 	self.pool.close()
	# 	self.pool.join()
	# 	logger.info('obtained news content and analysis done.')
	# 	return self.contents

	def get_all_news_content(self):
		logger.info('starting obtain news content for %s news by multi-threading' % len(self.input_data))
		threads = []
		for item in self.input_data:
			threads.append(Thread(target=self.__get_news_content_wrapper,
			                      kwargs={'url': item.get('url'),
			                              'create_ts': item.get('create_ts'),
			                              'title': item.get('title'),
			                              'published_time': item.get('published_time'),
			                              'sc_id': item.get('sc_id')
			                              }))

		[x.start() for x in threads]
		[x.join() for x in threads]

		logger.info('obtained news content and analysis done.')
		return self.contents


if __name__ == "__main__":
	pass
