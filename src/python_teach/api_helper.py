#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 创建人:李鸢
import requests
from requests import Timeout

from common.exceptions.api_exception import ApiException
from common.exceptions.data_exception import DataException
from scpy.logger import get_logger

logging = get_logger(__file__)


class ApiHelper(object):
    """
    api 辅助器
    """

    @staticmethod
    def get_url_dict(url):
        """
        get 请求返回字典表
        :type url str
        """
        try:
            logging.info('request:' + url)
            response = requests.get(url, timeout=120, headers={'Connection': 'keep-alive'})
            logging.info('response:' + url)
            return response.json() if response.ok else {}
        except Exception, e:
            logging.error('error url: %s', url)
            logging.error('error message: %s', e.message)
            raise DataException(inner_exception=e)

    @staticmethod
    def post_url_dict(url, data):
        """
        get 请求返回字典表
        :type url str
        """
        try:
            headers = {'content-type': 'application/json',
                       'Connection': 'keep-alive',
                       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

            logging.info('request:' + url)
            import json
            response = requests.post(url, data=json.dumps(data), timeout=120, headers=headers)
            logging.info('response:' + url)
            return response.json() if response.ok else {}
        except Timeout as e:
            logging.error('error url: %s', url)
            logging.error('error message: %s', e.message)
            raise ApiException(message=u"api请求超时", code=ApiException.CODE_TIMEOUT, inner_exception=e)
        except Exception, e:
            logging.error('error url: %s', url)
            logging.error('error message: %s', e.message)
            raise ApiException(message=u"api请求未知错误", inner_exception=e)


if __name__ == '__main__':
    from api.api_utils.api_helper import ApiHelper as apiH
    from conf.config import *
    import json

    res = apiH.get_url_dict(GET_CMP_BASIC_INFO + "北京龙盛源小额贷款有限公司")
    print (json.dumps(res, ensure_ascii=False, indent=4))
