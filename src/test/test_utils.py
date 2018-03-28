#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime    : 18-3-2 下午3:54
# @author  : 李鸢
import json
from common.utils.string_utils import StringUtils


class TestUtils(object):
    @staticmethod
    def my_print(*lists):
        """
        如果参数列表最后一位为 False 就拒绝打印
        """

        print StringUtils.decode(lists)

    @staticmethod
    def print_domain(obj):
        """
        领域对象打印
        """
        print json.dumps(obj, ensure_ascii=False, indent=4, default=lambda x: x.__dict__)

    @staticmethod
    def equal(var1, var2):
        """
        验证两个浮点数 对象是否大致相等
        """
        return var1 - var2 < 0.00001

    @staticmethod
    def assert_equal(expected, actual, message=''):
        if expected != actual:
            assert expected == actual, '{} 期待值:{} 实际值{}'.format(message, expected,actual)

    @staticmethod
    def side_effect(reason_dict, default_value):
        """
        返回一个mock 方法
        :param reason_dict: 第一个输入值，输出值匹配字典表
        :param default_value: 未匹配的默认值
        :return: 用于设置 相关mock的inner_effect属性
        """

        def inner_effect(*arg):
            input_name = arg[0]
            if input_name in reason_dict.keys():
                return reason_dict[input_name]
            else:
                return default_value

        return inner_effect
