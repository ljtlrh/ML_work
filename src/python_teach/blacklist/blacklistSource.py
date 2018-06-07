# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import sys
sys.path.append("../..")
reload(sys)

import os
import abc

from scpy.logger import get_logger

from utils.redis_tool import generate_redis_key, ONE_WEEK, ONE_YEAR
# import utils.redis_tool

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)
if CURRENT_PATH:
    CURRENT_PATH = CURRENT_PATH + '/'

from utils.redis_client import RedisHelper
from Queue import Queue


# from multiprocessing import Queue
# import multiprocessing


class Blacklist(object):
    def __init__(self):
        self.r = RedisHelper()
        self.use_cache = True
        self.cache_expire = ONE_YEAR
        self.cache_expire_isTrue = False
        self.company_info_queue = Queue()
        self.data_network = {}

    def set_cache(self, cache):
        self.use_cache = cache

    def set_cache_expire(self, cache_expire, is_true):
        self.cache_expire = cache_expire
        self.cache_expire_isTrue = is_true

    @abc.abstractmethod
    def get_results(self):
        raise NotImplementedError('call to abstract method %s.get_results' % self.__class__)

    def read_from_cache(self, company_name, cls=''):
        if not cls:
            cls = self.__class__.__name__
        if not isinstance(cls, str):
            raise TypeError('The cls paras should be a string. ')
        keys = generate_redis_key(company_name=company_name, cls=cls)
        if self.r.exists(keys):
            logger.info(' %s of %s found from redis.' % (cls, company_name))
            return self.r.get(keys)
        else:
            return None

    def save_to_cache(self, company_name, data, cls='', expired_days=ONE_WEEK):
        if not cls:
            cls = self.__class__.__name__
        if not isinstance(cls, str):
            raise TypeError('The cls paras should be a string. ')
        keys = generate_redis_key(company_name=company_name, cls=cls)
        if not isinstance(data, str):
            raise TypeError('The data has to be a string, try json.dumps method. ')
        self.r.set(keys, data)
        # 如果调用ＡＰＩ时设置了缓存时间就使用设置的缓存时间，否则使用默认时间，
        # cache_expire_isTrue为ｔｒｕｅ默认一年，也可以使用自定义的缓存周期
        if self.cache_expire_isTrue is True:
            self.r.expire(keys, self.cache_expire)
        else:
            self.r.expire(keys, expired_days)

    #格式公司名字的静态方法
    @staticmethod
    def get_company_names_from_network(network_data):
        if not isinstance(network_data, list):
            raise ValueError('The input of network should be a list')
         
        old_num = len(network_data)
        company_name_list = map(lambda x: x.get('companyName'), network_data)
        # 去重
        company_name_list = list(set(company_name_list))
        
        # 去除空
        company_name_list = filter(lambda x: True if x else False, company_name_list)
        logger.info('%s duplicated company name(s) are removed from network' % (old_num - len(company_name_list)))
        return company_name_list

    @abc.abstractmethod
    def data_validation(self, **kwargs):
        raise NotImplementedError('call to abstract method %s.get_results' % self.__class__)


if __name__ == "__main__":
    b = Blacklist()
    res = b.read_from_cache(u'测试')
    print res
