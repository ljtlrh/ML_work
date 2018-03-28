#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime    : 18-3-1 下午4:51
# @author  : 李鸢
import json


from scpy.kv_helper import set_hierachical_kv


class JsonUtils(object):
    """
    json 工具类
    """

    @staticmethod
    def get_val(contents, key_list, default=None):
        """
        返回指定子集的值
        """
        if not contents:
            return default
        if isinstance(key_list, list):
            for idx, key in enumerate(key_list):
                # contents需要一直是dict类型（除了最后一个key的结果），不然无法get
                if not isinstance(contents, dict) or contents == {}:
                    contents = default
                    break
                contents = contents.get(key, default)
        else:  # 按传入key_list 为一单独字串处理
            contents = contents.get(key_list, default)
        # 最后一次get的结果需要不为None|''|[]|{}，否则以default返回
        if contents is None:
            contents = default
        return contents

    @staticmethod
    def collect_2_json_str(dict_obj):
        """
        dict or list 转换json
        """
        return json.dumps(dict_obj, ensure_ascii=False)

    @staticmethod
    def domain_2_json_str(obj):
        """
        领域对象转换json 字串
        """
        return json.dumps(obj, ensure_ascii=False, default=lambda x: x.__dict__)

    @staticmethod
    def str_2_collect(str_obj):
        """
        json 转换 dict or list
        """
        return json.loads(str_obj)


    @staticmethod
    def set_val(contents, key_list, default=None):
        """
        返回指定子集的值
        """
        if default is None:
            default = {}
        set_hierachical_kv(contents, key_list, default)

    @staticmethod
    def save_json_file(path, file_name, data):
        with open(path + '/' + file_name, 'w') as json_file:
            json_file.write(json.dumps(data))

    @staticmethod
    def save_json_file_append(path, file_name, data):
        with open(path + '/' + file_name, 'a') as json_file:
            json_file.write(json.dumps(data))
            json_file.write(',\n')

    @staticmethod
    def load_json_file(path, file_name):
        with open(path + '/' + file_name) as json_file:
            data = json.load(json_file)
            return data

