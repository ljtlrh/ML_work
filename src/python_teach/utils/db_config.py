#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
全局变量，配置文件
Created on 2017年11月21日
@author: ljt
'''

import sys

sys.path.append('../..')
from scpy.xawesome_codechecker import get_ip
from scpy.logger import get_logger

logger = get_logger(__file__)

MYSQL_HOST = '116.196.120.26'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'axzsd110'
MYSQL_DATABASE = 'cpmdb'
MYSQL_PORT = 3306
DB_CHAR ='utf8'
csvpath= "data01/user_product_rating.csv"
product_feature_path = "data01/product_feature.csv"
product_Similar_path = "data01/product_Similar.json"
user_product_rating_path = "data01/user_product_rating.csv"

if get_ip().startswith('172.16') or get_ip().startswith('192.168'):

	# PG_HOST = '192.168.31.157'
	# PG_USER = 'tas_local'
	# PG_PASSWORD = '1qaz2wsx'
	# PG_DATABASE = 'tas_local'
	# PG_PORT = '5432'


    PG_HOST = '111.231.195.27'
    # PG_HOST = '127.0.0.1'
    PG_USER = 'tas_prod'
    PG_PASSWORD = '1qaz2wsx'
    PG_DATABASE = 'tas_prod'
    PG_PORT = '5432'

else:
    # PG_HOST = '111.231.195.27'
    PG_HOST = '127.0.0.1'
    PG_USER = 'tas_prod'
    PG_PASSWORD = '1qaz2wsx'
    PG_DATABASE = 'tas_prod'
    PG_PORT = '5432'
