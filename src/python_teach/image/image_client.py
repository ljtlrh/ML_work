#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: image_client.py
@time: 18-5-3 下午6:07
"""
#encoding=utf8
import sys
# import os
# import time
import base64
import argparse
import json
import requests
import cv2

reload(sys)
sys.setdefaultencoding('utf8')


def get_args():
    '''get args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', default="../image/1.jpg")
    return parser.parse_args()

def main():
    '''main function
    '''
    args = get_args()
    in_file = args.image

    # post imagefile
    host = "http://127.0.0.1:9123/service_demo"
    img_file = open(in_file, "rb").read()

    data = {}
    data["image_base64"] = base64.b64encode(img_file)

    result = requests.post(host, json=data)
    print result
    result = json.loads(result.text)
    print result


if __name__ == "__main__":
    main()