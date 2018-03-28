#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 创建人:李鸢
import json
import re


import sys

import datetime
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")

class StringUtils(object):
    """
    字串工具集
    """

    @staticmethod
    def is_none(d):
        '''
        判断字符串是否为空包括‘’，NULL，,None
        :param d:
        :return:
        '''
        return (d is None or d == 'None' or
                d == '' or
                d == {} or
                d == [] or
                d == 'NULL' or
                d == 'null')

    @staticmethod
    def last_word_cut(text):
        """
        剪接最后一个字符
        """
        text = text[:len(text) - 1]
        return text

    @staticmethod
    def is_in_str(str_list, trg_str):
        is_find = False

        if trg_str:
            for s in str_list:
                if s in trg_str:
                    is_find = True
                    break
            # end for
        # end if

        return is_find

    @staticmethod
    def right_cut_by_word(text, cut_word):
        """
        右向剪断字符
        input: text= 'good/bye/oo', cut_word = 'bye'
        output: 'good/'
        """
        i = text.find(cut_word)
        if i != -1:
            text = text[0: i]

        return text

    @staticmethod
    def last_word_cut_num(text, cut_num):
        """
        剪接最后指定数量字符
        """
        text = text[:len(text) - cut_num]
        return text

    @staticmethod
    def str_q2b(ustring):
        """全角转半角"""

        ustring = ustring.encode('utf-8').decode('utf-8')

        r_string = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            r_string += unichr(inside_code)
        return r_string

    @staticmethod
    def get_replace_pattern(text_parts, context, str_to_replace=u''):
        """
        正则替换匹配值为空
        :param text_parts:
        :param context:
        :param str_to_replace:
        :return:
        """
        context = context.encode('utf-8').decode('utf-8')
        return re.sub(text_parts, str_to_replace, context)

    @staticmethod
    def decode(input_str):
        """
        中文解码
        """
        return json.dumps(input_str, ensure_ascii=False, indent=4, default=lambda x: str(x))

    @staticmethod
    def contain_var_in_string(containVar, stringVar):
        '''
        python判断字符串中包含某个字符的判断函数脚本
        :param containVar:查找包含的字符
        :param stringVar:所要查找的字符串
        :return:
        '''
        if isinstance(stringVar, str):
            if containVar in stringVar:
            # if stringVar.find(containVar) > -1:
                return True
            else:
                return False
        else:
            return False


if __name__=="__main__":

    start = datetime.datetime.now()
    if StringUtils.contain_var_in_string("111","我|111发现_推荐|我听|发现"):
        print "0:00:00.000021"
    print("sss=>"+str(datetime.datetime.now() - start))